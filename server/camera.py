import threading
import binascii
from time import sleep
from get_gestures_from_webcam import get_gestures_from_webcam as gestures
from utils import base64_to_pil_image, pil_image_to_base64, to_cv2
from get_gestures_from_webcam.gestures import Gesture
import base64
from io import BytesIO



class Camera(object):
    def __init__(self):
        self.to_process = []
        self.to_output = []
        self.gestures = Gesture()

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.to_process:
            #print(len(self.to_process))
            return

        # Input is an ascii string.
        input_str = self.to_process.pop(0)

        # Convert it to a cv2 image
        input_img = to_cv2(input_str)

        # Get the gestures.
        output_img = self.gestures.get_gesture_from_webcam(input_img)

        # convert eh base64 string in ascii to base64 string in _bytes_
        #self.to_output.append(binascii.a2b_base64(output_str))
        self.to_output.append(output_img)

    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.001)

    def enqueue_input(self, input):
        self.to_process.append(input)
        # self.process_one()

    def get_frame(self):
        while not self.to_output:
            sleep(0.001)
        return self.to_output.pop(0)