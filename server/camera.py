import threading
from time import sleep
from utils import to_cv2
from get_gestures_from_webcam.gestures import GestureRecognition


class Camera(object):
    def __init__(self):
        self.to_process = []
        self.to_output = []
        self.gestures = GestureRecognition()

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.to_process:
            # print(len(self.to_process))
            return

        # Input is an ascii string.
        input_str = self.to_process.pop(0)

        # Convert it to a cv2 image
        input_img = to_cv2(input_str)

        # Get the gestures.
        output_img = self.gestures.get_gesture_from_webcam(input_img)

        # Send the annotated image.
        self.to_output.append(output_img)

    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.0001)

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
