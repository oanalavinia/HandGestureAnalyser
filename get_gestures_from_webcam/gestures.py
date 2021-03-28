import mediapipe as mp
import cv2
from get_gestures_from_webcam import utilities as ut
from get_gestures_from_webcam import owl_utilities, wave_gesture
from owl_testing import test_owl as owl
from datetime import datetime


class Gesture(object):
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.gesture = 'none'

        self.last_gestures = ['none']
        self.user = owl.User()
        self.owl_utilities = owl_utilities.Owl_utilities()
        self.recording_start_time = datetime.now()

        # Variables needed for registering wave gesture.
        self.wave_gesture_time = datetime.now()
        self.wave_gesture_identifier = wave_gesture.WaveGesture()
        # set_record(True)

    def get_gesture_from_landmarks(self, landmarks_x, landmarks_y):
        #
        # We only take gestures from one hand.
        #
        is_reversed = False
        is_wave_gesture = False
        if len(landmarks_x) != 0:
            # Wave gesture is handled individually since it is a movement gestures, not a static one.
            # is_wave_gesture = self.wave_gesture_identifier.get_wave_gesture(landmarks_x, landmarks_y)

            is_reversed = ut.is_reversed(landmarks_x)
            self.gesture = ut.get_gestures(landmarks_x=landmarks_x, landmarks_y=landmarks_y, is_reversed=is_reversed)
            if is_wave_gesture:
                self.gesture = "wave"
                self.wave_gesture_time = datetime.now()
            #
            if len(self.last_gestures) > 55:
                self.last_gestures.pop(0)
            self.last_gestures.append(self.gesture)
        else:
            self.last_gestures = ['none']

        # Make an average from the last 50 frames. If a wave gesture was registered, consider only this one for 3
        # seconds.
        if self.wave_gesture_time and (datetime.now() - self.wave_gesture_time).seconds < 3:
            self.gesture = "wave"

        else:
            self.gesture = ut.most_frequent(self.last_gestures)

        # Create rdf instance
        self.create_rdf_instances(self.gesture)

        # We save data every 10 seconds.
        if (datetime.now() - self.recording_start_time).seconds > 10:
            self.recording_start_time = datetime.now()
            self.owl_utilities.save_data()
            # last_10_gesture = qrs.query_last_10s_gestures(datetime.now())
            # save_data()

        return self.gesture

    def get_gesture_from_webcam(self, frame):

        # Flip the image horizontally for a later selfie-view display, and convert the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False
        results = self.hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True

        #
        # Save all hands.
        #
        hands_landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hands_landmarks.append(hand_landmarks)
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        #
        # We only take gestures from one hand.
        #
        landmarks = []
        is_reversed = False
        is_wave_gesture = False
        if len(hands_landmarks) != 0:
            for data_point in hands_landmarks[0].landmark:
                landmarks.append({
                    'x': data_point.x,
                    'y': data_point.y,
                    'z': data_point.z,
                    'Visibility': data_point.visibility,
                })

            # Wave gesture is handled individually since it is a movement gestures, not a static one.
            is_wave_gesture = self.wave_gesture_identifier.get_wave_gesture(landmarks)

            is_reversed = ut.is_reversed(landmarks)
            self.gesture = ut.get_gestures(landmarks=landmarks, is_reversed=is_reversed)
            if is_wave_gesture:
                self.gesture = "wave"
                self.wave_gesture_time = datetime.now()
            #
            if len(self.last_gestures) > 55:
                self.last_gestures.pop(0)
            self.last_gestures.append(self.gesture)
        else:
            self.last_gestures = ['none']

        # Make an average from the last 50 frames. If a wave gesture was registered, consider only this one for 3
        # seconds.
        if self.wave_gesture_time and (datetime.now() - self.wave_gesture_time).seconds < 3:
            self.gesture = "wave"

        else:
            self.gesture = ut.most_frequent(self.last_gestures)

        # Create rdf instance
        self.create_rdf_instances(self.gesture)

        # We save data every 10 seconds.
        if (datetime.now() - self.recording_start_time).seconds > 10:
            self.recording_start_time = datetime.now()
            self.owl_utilities.save_data()
            # last_10_gesture = qrs.query_last_10s_gestures(datetime.now())
            # save_data()

        (_, encodedImage) = cv2.imencode(".jpg",
                                         cv2.putText(image, self.gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                     (255, 0, 0),
                                                     2, cv2.LINE_AA))

        return encodedImage

    def create_rdf_instances(self, gesture):
        gest = self.owl_utilities.get_gesture_instance(gesture)
        if gest:
            gest.has_gesture_time.append(datetime.now())
            gest.has_gesture_name.append(gesture)
            self.user.makes_gesture.append(gest)
        return gest
