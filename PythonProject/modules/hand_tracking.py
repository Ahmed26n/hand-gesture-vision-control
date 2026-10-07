import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import math
import urllib.request
import os


class HandDetector:
    def __init__(self, max_hands=1, detection_con=0.7, track_con=0.7):
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con
        self.tip_ids = [4, 8, 12, 16, 20]

        # Download model task file if not present
        self.model_path = "hand_landmarker.task"
        if not os.path.exists(self.model_path):
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            urllib.request.urlretrieve(url, self.model_path)

        # Initialize HandLandmarker Task
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=self.max_hands,
            min_hand_detection_confidence=self.detection_con,
            min_hand_presence_confidence=self.track_con
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.results = None
        self.lm_list = []

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        self.results = self.detector.detect(mp_image)

        if draw and self.results.hand_landmarks:
            h, w, c = img.shape
            for hand_lms in self.results.hand_landmarks:
                for lm in hand_lms:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                # Draw connection lines between landmarks
                connections = [
                    (0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8),
                    (5, 9), (9, 10), (10, 11), (11, 12), (9, 13), (13, 14), (14, 15), (15, 16),
                    (13, 17), (17, 18), (18, 19), (19, 20), (0, 17)
                ]
                for p1, p2 in connections:
                    x1, y1 = int(hand_lms[p1].x * w), int(hand_lms[p1].y * h)
                    x2, y2 = int(hand_lms[p2].x * w), int(hand_lms[p2].y * h)
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return img

    def find_positions(self, img, hand_no=0):
        self.lm_list = []
        if self.results and self.results.hand_landmarks:
            if hand_no < len(self.results.hand_landmarks):
                my_hand = self.results.hand_landmarks[hand_no]
                h, w, c = img.shape
                for lm_id, lm in enumerate(my_hand):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lm_list.append([lm_id, cx, cy])
        return self.lm_list

    def fingers_up(self):
        fingers = []
        if not self.lm_list:
            return fingers

        # Thumb
        if self.lm_list[self.tip_ids[0]][1] < self.lm_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for tip_id in range(1, 5):
            if self.lm_list[self.tip_ids[tip_id]][2] < self.lm_list[self.tip_ids[tip_id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def find_distance(self, p1, p2, img, draw=True):
        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]
        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x2 - x1, y2 - y1)

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

        return length, img, [x1, y1, x2, y2, cx, cy]