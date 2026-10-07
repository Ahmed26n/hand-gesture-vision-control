# Hand Gesture Vision Control
#### Video Demo: [Watch the Video Demo on YouTube](https://youtu.be/CWx7rwzWSRE)

## Description
**Hand Gesture Vision Control** is an intuitive computer vision application built in Python that allows users to seamlessly control mouse movements, perform clicks, and navigate desktop interfaces using hand gestures captured via a standard webcam. Developed as the final project for Harvard University's CS50x, this application provides an interactive and touchless virtual trackpad experience with a dark holographic visual interface.

The project leverages **OpenCV** for real-time video stream capture and image manipulation, **MediaPipe** for accurate 21-point hand landmark detection, **PyAutoGUI** for high-responsiveness mouse control, **NumPy** for custom holographic landmark rendering on a pitch-black background, and **Tkinter** to display an initial setup and instruction guide.

---

## Key Features
- **Holographic Visual Interface:** Renders hand landmarks and skeletal structures with vibrant neon cyan and yellow aesthetics against a pure black background for a clean look.
- **Relative Trackpad Control Mode:** Raising only the index finger maps hand movement relative to its previous position, enabling smooth and accurate cursor positioning across high-resolution displays.
- **Gesture Action Triggers:**
  - **Cursor Movement:** Raising ONLY the Index Finger.
  - **Left Click:** Raising Index and Middle fingers and pinching them together.
  - **Right Click:** Pinching Thumb and Index finger together.
  - **Pause / Reset Position:** Making a Fist pauses tracking, allowing the user to reposition their hand without moving the cursor.
- **Graphical User Interface (GUI):** Integrated Tkinter window detailing instructions and control mapping prior to launching the camera feed.
- **Jitter & Speed Optimization:** Configured zero-delay PyAutoGUI settings alongside relative coordinate calculation and motion smoothing to eliminate cursor jitter.

---

## File Structure
- `main.py`: Main application script containing the Tkinter instructions window, webcam video processing loop, relative movement math, and holographic landmark renderer.
- `modules/hand_tracking.py`: Custom module wrapping MediaPipe's Hand solution for initialization, coordinate normalization, landmark extraction, and finger state detection.
- `requirements.txt`: List of dependencies required to run the project (`opencv-python`, `mediapipe`, `pyautogui`, `numpy`).
- `README.md`: Detailed documentation of the project structure, features, and setup instructions.

---

## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Ahmed26n/hand-gesture-vision-control.git](https://github.com/Ahmed26n/hand-gesture-vision-control.git)
   cd hand-gesture-vision-control