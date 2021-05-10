from time import sleep
from get_gestures_from_webcam.gestures import GestureRecognition


class Camera(object):
    def __init__(self):
        self.to_process = []
        self.to_output = []
        self.gestures = GestureRecognition()

    def enqueue_input(self, input):
        self.to_process.append(input)

    def get_frame(self):
        while not self.to_output:
            sleep(0.001)
        return self.to_output.pop(0)

    def get_gesture(self):
        return self.gestures.gesture

    def get_gesture_obj(self):
        return self.gestures
