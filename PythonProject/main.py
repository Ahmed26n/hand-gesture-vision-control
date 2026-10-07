import cv2
import numpy as np
import pyautogui
import tkinter as tk
from modules.hand_tracking import HandDetector


def launch_instructions_window():
    """Displays the initial GUI with controls and instructions."""
    root = tk.Tk()
    root.title("Hand Gesture Vision Control - CS50x")
    root.geometry("600x520")
    root.resizable(True, True)
    root.configure(bg="#1E1E2E")

    # Title Banner
    title_label = tk.Label(
        root,
        text="Hand Gesture Controller",
        font=("Helvetica", 18, "bold"),
        fg="#89B4FA",
        bg="#1E1E2E",
        pady=10
    )
    title_label.pack()

    subtitle_label = tk.Label(
        root,
        text="CS50x Final Project Guide",
        font=("Helvetica", 11, "italic"),
        fg="#A6ADC8",
        bg="#1E1E2E"
    )
    subtitle_label.pack()

    # Instructions Frame
    instructions_frame = tk.LabelFrame(
        root,
        text=" How to Use ",
        font=("Helvetica", 12, "bold"),
        fg="#CDD6F4",
        bg="#313244",
        padx=15,
        pady=10
    )
    instructions_frame.pack(padx=20, pady=15, fill="both", expand=True)

    instructions_text = (
        "1. Cursor Movement:\n"
        "   Raise ONLY your Index Finger to move the mouse (Trackpad Mode).\n\n"
        "2. Left Click:\n"
        "   Raise Index & Middle Fingers together and pinch them close.\n\n"
        "3. Right Click:\n"
        "   Pinch Thumb and Index Finger close together.\n\n"
        "4. Pause / Reset Position:\n"
        "   Make a Fist to pause tracking, reposition your hand, then raise Index Finger."
    )

    lbl_info = tk.Label(
        instructions_frame,
        text=instructions_text,
        font=("Segoe UI", 10),
        fg="#CDD6F4",
        bg="#313244",
        justify="left"
    )
    lbl_info.pack(anchor="w")

    # Start Button Callback
    def start_program():
        root.destroy()

    start_button = tk.Button(
        root,
        text="Start System",
        font=("Helvetica", 12, "bold"),
        bg="#A6E3A1",
        fg="#11111B",
        activebackground="#94E2D5",
        padx=15,
        pady=8,
        command=start_program,
        cursor="hand2"
    )
    start_button.pack(pady=15)

    root.mainloop()


# 1. Launch GUI Instructions Window
launch_instructions_window()

# 2. PyAutoGUI Optimization
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
pyautogui.MINIMUM_DURATION = 0

screen_width, screen_height = pyautogui.size()

# Camera & Frame Settings
cap = cv2.VideoCapture(0)
cam_width, cam_height = 640, 480
cap.set(3, cam_width)
cap.set(4, cam_height)

# High-Speed Parameters
sensitivity = 4.5
smoothening = 3.0

# Tracking Variables
prev_cam_x, prev_cam_y = 0.0, 0.0
curr_mouse_x, curr_mouse_y = float(pyautogui.position()[0]), float(pyautogui.position()[1])
is_tracking = False

detector = HandDetector(max_hands=1, detection_con=0.7)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)

    # إنشاء خلفية سوداء بالكامل بنفس حجم الإطار
    h, w, c = img.shape
    hologram_img = np.zeros((h, w, c), dtype=np.uint8)

    # تتبع اليد بدون الرسم التلقائي على الصورة
    img = detector.find_hands(img, draw=False)
    lm_list = detector.find_positions(img)

    if lm_list:
        # رسم الهيكل العظمي بنمط هولوغرام (Cyan / Neon Blue)
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # الإبهام
            (0, 5), (5, 6), (6, 7), (7, 8),  # السبابة
            (5, 9), (9, 10), (10, 11), (11, 12),  # الوسطى
            (9, 13), (13, 14), (14, 15), (15, 16),  # البنصر
            (13, 17), (17, 18), (18, 19), (19, 20),  # الخنصر
            (0, 17)  # أسفل الكف
        ]

        for p1, p2 in connections:
            pt1 = (int(lm_list[p1][1]), int(lm_list[p1][2]))
            pt2 = (int(lm_list[p2][1]), int(lm_list[p2][2]))
            cv2.line(hologram_img, pt1, pt2, (255, 255, 0), 2)  # خطوط سيان نيون

        for lm in lm_list:
            cx, cy = int(lm[1]), int(lm[2])
            cv2.circle(hologram_img, (cx, cy), 4, (0, 255, 255), cv2.FILLED)  # نقاط صفراء نيون

        raw_x, raw_y = float(lm_list[8][1]), float(lm_list[8][2])
        fingers = detector.fingers_up()

        # 1. Moving Mode: ONLY Index Finger UP
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            if not is_tracking:
                prev_cam_x, prev_cam_y = raw_x, raw_y
                curr_mouse_x, curr_mouse_y = float(pyautogui.position()[0]), float(pyautogui.position()[1])
                is_tracking = True

            dx = (raw_x - prev_cam_x) * sensitivity
            dy = (raw_y - prev_cam_y) * sensitivity

            target_mouse_x = curr_mouse_x + dx
            target_mouse_y = curr_mouse_y + dy

            curr_mouse_x += (target_mouse_x - curr_mouse_x) / smoothening
            curr_mouse_y += (target_mouse_y - curr_mouse_y) / smoothening

            curr_mouse_x = max(0.0, min(float(screen_width - 1), curr_mouse_x))
            curr_mouse_y = max(0.0, min(float(screen_height - 1), curr_mouse_y))

            pyautogui.moveTo(int(curr_mouse_x), int(curr_mouse_y))
            # مؤشر الحركة نيون وردي متوهج
            cv2.circle(hologram_img, (int(raw_x), int(raw_y)), 10, (255, 0, 255), cv2.FILLED)

            prev_cam_x, prev_cam_y = raw_x, raw_y

        else:
            is_tracking = False

        # 2. Left Click Mode: Index & Middle UP
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            length, _, line_info = detector.find_distance(8, 12, img)
            if length < 38:
                cv2.circle(hologram_img, (line_info[4], line_info[5]), 12, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

        # 3. Right Click Mode: Thumb & Index UP
        elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            length, _, line_info = detector.find_distance(4, 8, img)
            if length < 28:
                cv2.circle(hologram_img, (line_info[4], line_info[5]), 12, (0, 0, 255), cv2.FILLED)
                pyautogui.rightClick()

    else:
        is_tracking = False

    # عرض النافذة بنمط الهولوغرام على خلفية سوداء
    cv2.imshow("Hand Gesture Controller", hologram_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()