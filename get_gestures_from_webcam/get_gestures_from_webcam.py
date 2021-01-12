import cv2
import mediapipe as mp
import utilities as ut

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
last_gestures = ['none']

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

    # Save all hands.
    hands_landmarks = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            hands_landmarks.append(hand_landmarks)
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # We only take gestures from one hand for now.
    landmarks = []
    is_reversed = False
    if len(hands_landmarks) != 0:
        for data_point in hands_landmarks[0].landmark:
            landmarks.append({
                'x': data_point.x,
                'y': data_point.y,
                'z': data_point.z,
                'Visibility': data_point.visibility,
            })

        is_reversed = ut.is_reversed(landmarks)
        gesture = ut.get_fingers(landmarks=landmarks, is_reversed=is_reversed)
        if len(last_gestures) > 9:
            last_gestures.pop(0)
        last_gestures.append(gesture)
    else:
        last_gestures = ['none']

    # Make an average from the last 10 frames.
    gesture = ut.most_frequent(last_gestures)
    cv2.imshow('Hands', cv2.putText(image, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA))

    # Stopping.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

hands.close()
cap.release()
