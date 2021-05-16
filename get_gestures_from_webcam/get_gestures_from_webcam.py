import cv2
import mediapipe as mp
from datetime import datetime
from get_gestures_from_webcam import utilities as ut
from owl import ontology_manipulations as owl
from scripts import queries as qrs

def get_gestures(cap):
    user1 = owl.User()
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    record = True

    hands = mp_hands.Hands(
        min_detection_confidence=0.5, min_tracking_confidence=0.5)
    last_gestures = ['none']
    # Variables needed for registering wave gesture.
    temporary_wave_gestures = []
    last_hand_x_position = 0
    wave_frames = 0
    wave_gesture_time = datetime.now()
    set_record(True)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #
        # Save all hands.
        #
        hands_landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hands_landmarks.append(hand_landmarks)
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        #
        # We only take gestures from one hand.
        #
        landmarks = []
        is_reversed = False
        wave_gesture = False
        if len(hands_landmarks) != 0:
            for data_point in hands_landmarks[0].landmark:
                landmarks.append({
                    'x': data_point.x,
                    'y': data_point.y,
                    'z': data_point.z,
                    'Visibility': data_point.visibility,
                })

            # Wave gesture is handled individually since it is a movement gestures, not a static one.
            wave_gesture, last_hand_x_position, temporary_wave_gestures, wave_frames = ut.get_wave_gesture(landmarks,
                                                                                                           wave_frames,
                                                                                                           last_hand_x_position,
                                                                                                           temporary_wave_gestures)

            is_reversed = ut.is_reversed(landmarks)
            gesture = ut.get_gestures(landmarks=landmarks, is_reversed=is_reversed)
            if wave_gesture:
                gesture = "wave"
                wave_gesture_time = datetime.now()

            if len(last_gestures) > 59:
                last_gestures.pop(0)
            last_gestures.append(gesture)
        else:
            last_gestures = ['none']

        # Make an average from the last 50 frames. If a wave gesture was registered, consider only this one for 3
        # seconds.
        if wave_gesture_time and (datetime.now() - wave_gesture_time).seconds < 3:
            gesture = "wave"

        else:
            gesture = ut.most_frequent(last_gestures)

        # Create rdf instance
        # create_rdf_instances(gesture, user1)

        (_, encodedImage) = cv2.imencode(".jpg",
                                         cv2.putText(image, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                                                     2, cv2.LINE_AA))

        # We save data every 10 seconds.
        if (datetime.now() - recording_start_time).seconds > 10:
            recording_start_time = datetime.now()
            # save_data()
            last_10_gesture = qrs.query_last_10s_gestures(datetime.now())
            # save_data()

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

    hands.close()


def save_data():
    global record
    if record is not None and record is True:
        print("saving data..")
        with open("../rdf_data/test.xml", 'wb') as f:
            owl.fiiGezr.save(file=f, format="rdfxml")


def set_record(val):
    global record
    record = val


def get_record():
    global record
    return record

# useScript()
