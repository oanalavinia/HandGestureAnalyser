from get_gestures_from_webcam import utilities as ut
from get_gestures_from_webcam import owl_utilities, wave_gesture
from owl import ontology_manipulations as owl
from datetime import datetime


class GestureRecognition(object):
    def __init__(self):
        self.gesture = 'none'
        self.last_gestures = ['none']
        self.user = owl.User()
        self.owl_utilities = owl_utilities.Owl_utilities()
        self.recording_start_time = datetime.now()
        self.context = "none"
        self.owl_context = "none"
        self.gesture_time = datetime.now()

        # Variables needed for registering wave gesture.
        self.wave_gesture_time = datetime.now()
        self.wave_gesture_identifier = wave_gesture.WaveGesture()
        # set_record(True)

    def get_gesture_from_landmarks(self, landmarks_x, landmarks_y):
        is_reversed = False
        is_wave_gesture = False
        if len(landmarks_x) != 0:
            # Wave gesture is handled individually since it is a movement gestures, not a static one.
            is_wave_gesture = self.wave_gesture_identifier.get_wave_gesture(landmarks_x, landmarks_y)

            is_reversed = ut.is_reversed(landmarks_x)
            self.gesture = ut.get_gestures(landmarks_x=landmarks_x, landmarks_y=landmarks_y, is_reversed=is_reversed)
            if is_wave_gesture:
                self.gesture = "wave"
                self.wave_gesture_time = datetime.now()

            #
            if len(self.last_gestures) == 40:
                self.gesture_time = datetime.now()

            if len(self.last_gestures) >= 40:
                self.last_gestures = []

            if (datetime.now() - self.gesture_time).seconds > 0.5:
                self.last_gestures.append(self.gesture)

            if len(self.last_gestures) < 40:
                return 'none'
        else:
            self.last_gestures = ['none']

        self.gesture_time = datetime.now()
        # Make an average from the last 70 frames. If a wave gesture was registered, consider only this one for 3
        # seconds.
        if self.wave_gesture_time and (datetime.now() - self.wave_gesture_time).seconds < 3:
            self.gesture = "wave"
        else:
            self.gesture = ut.most_frequent(self.last_gestures)

        self.create_rdf_instances()

        # We save data every 10 seconds.
        # if (datetime.now() - self.recording_start_time).seconds > 10:
        #     self.recording_start_time = datetime.now()
        #     self.owl_utilities.save_data()
        #     # last_10_gesture = qrs.query_last_10s_gestures(datetime.now())
        #     # save_data()

        return self.gesture

    def create_rdf_instances(self):
        gest = self.owl_utilities.get_gesture_instance(self.gesture)
        if gest:
            gest.hasGestureTime = datetime.now()
            gest.hasGestureName = self.gesture
            self.user.makesGesture.append(gest)
            #if self.context != "none":
                #self.owl_utilities.get_contexted_rule(self.context, self.gesture, self.owl_context)
        return gest

    def set_context(self, given_context):
        self.context = given_context
        if self.context == "QuizGame":
            self.owl_context = owl.QuizGame()
        elif self.context == "PDFDocument":
            self.owl_context = owl.PDFDocument()
        elif self.context == "Image":
            self.owl_context = owl.Image()
        elif self.context == "SelectionGame":
            self.owl_context = owl.SelectionGame()

    def create_rule_instance(self, gesture):
        self.owl_utilities.get_contexted_rule(self.context, gesture, self.owl_context)

    def get_owl_utilities(self):
        return self.owl_utilities

    def get_context(self):
        return self.context

    def get_owl_context(self):
        return self.owl_context
