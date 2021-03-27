import mediapipe as mp
import cv2
from get_gestures_from_webcam import utilities as ut
from get_gestures_from_webcam import owl_utilities
from owl_testing import test_owl as owl
from datetime import datetime

class Zoom_In_Gesture(object):
    def __init__(self):
        self.temporary_wave_gestures = []
        self.last_hand_x_position = 0
        self.wave_frames = 0
        self.wave_gesture_time = datetime.now()

    def get_wave_gesture(self, landmarks):
        this_hand_x_position = landmarks[8]['x']
        if abs(self.last_hand_x_position - this_hand_x_position) > 0.15:
            self.temporary_wave_gestures.append(True)
            self.last_hand_x_position = this_hand_x_position
        else:
            self.wave_frames += 1
        # If we found 7 wave gestures in the last max 20 frames where no wave was made.
        if len(self.temporary_wave_gestures) == 7:
            aux_frames = self.wave_frames
            self.wave_frames = 0
            self.temporary_wave_gestures = []
            if aux_frames < 20:
                return True

        return False




