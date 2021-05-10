def get_gestures(landmarks_x, landmarks_y, is_reversed):
    #
    # Get fingers orientation
    #
    thumb_closer, thumb_up, index_up, second_up, third_up, pinky_up = get_fingers_orientation(landmarks_x, landmarks_y, is_reversed)

    #
    # Simple gestures
    #
    gesture = check_count_gestures(thumb_closer, index_up, second_up, third_up, pinky_up)

    #
    # Get more information about hand
    #
    thumb_up_oriented, thumb_in_fist, four_fingers_closed = get_hand_info(landmarks_x, landmarks_y)

    # Get more gestures.
    if thumb_in_fist and four_fingers_closed:
        gesture = "fist"

    if thumb_up_oriented and not thumb_in_fist and four_fingers_closed:
        gesture = "thumbsDown"

    if not thumb_up_oriented and not thumb_in_fist and four_fingers_closed:
        gesture = "thumbsUp"

    # print("thumb {} index {}".format(thumb_up, index_up))
    if thumb_up and index_up and isZoomOutDistance(landmarks_x) and not(second_up or third_up or pinky_up):
        gesture = "zoomOut"

    if thumb_up and index_up and isZoomInDistance(landmarks_x) and not(second_up or third_up or pinky_up):
        gesture = "zoomIn"

    return gesture


def isZoomOutDistance(landmarks_x):
    return abs(landmarks_x[8] - landmarks_x[4]) < 0.17


def isZoomInDistance(landmarks_x):
    return abs(landmarks_x[8] - landmarks_x[4]) > 0.17


def get_hand_info(landmarks_x, landmarks_y):
    right_hand = True
    if landmarks_x[0] < landmarks_x[13]:
        right_hand = False

    pseudo_fix_key = landmarks_y[2]
    thumb_up_oriented = True
    if landmarks_y[3] < pseudo_fix_key and landmarks_y[4] < pseudo_fix_key:
        thumb_up_oriented = False

    thumb_in_fist = True
    if abs(landmarks_y[6] - landmarks_y[4]) > 0.16:
        thumb_in_fist = False

    # We check to see if the four fingers are closed together, considering the hand used
    if not right_hand:
        four_fingers_closed = False
        if landmarks_x[6] - landmarks_x[5] > landmarks_x[8] - landmarks_x[5] and \
                landmarks_x[10] - landmarks_x[9] > landmarks_x[12] - landmarks_x[9] and \
                landmarks_x[14] - landmarks_x[13] > landmarks_x[16] - landmarks_x[13] and \
                landmarks_x[18] - landmarks_x[17] > landmarks_x[20] - landmarks_x[17]:
            four_fingers_closed = True
    else:
        four_fingers_closed = False
        if landmarks_x[6] - landmarks_x[5] <= landmarks_x[8] - landmarks_x[5] and \
                landmarks_x[10] - landmarks_x[9] <= landmarks_x[12] - landmarks_x[9] and \
                landmarks_x[14] - landmarks_x[13] <= landmarks_x[16] - landmarks_x[13] and \
                landmarks_x[18] - landmarks_x[17] <= landmarks_x[20] - landmarks_x[17]:
            four_fingers_closed = True

    return thumb_up_oriented, thumb_in_fist, four_fingers_closed


#
# Check which fingers are up oriented.
#
def get_fingers_orientation(landmarks_x, landmarks_y, is_reversed):
    thumb_closer = False
    thumb_up = False
    index_up = False
    second_up = False
    third_up = False
    pinky_up = False

    pseudo_fix_key = landmarks_x[2]
    if not is_reversed:
        if landmarks_x[3] < pseudo_fix_key and landmarks_x[4] < pseudo_fix_key:
            thumb_closer = True
    else:
        if landmarks_x[3] > pseudo_fix_key and landmarks_x[4] > pseudo_fix_key:
            thumb_closer = True

    pseudo_fix_key = landmarks_y[2]
    if landmarks_y[3] < pseudo_fix_key and landmarks_y[4] < pseudo_fix_key:
        thumb_up = True

    pseudo_fix_key = landmarks_y[6]
    if landmarks_y[7] < pseudo_fix_key and landmarks_y[8] < pseudo_fix_key:
        index_up = True

    pseudo_fix_key = landmarks_y[10]
    if landmarks_y[11] < pseudo_fix_key and landmarks_y[12] < pseudo_fix_key:
        second_up = True

    pseudo_fix_key = landmarks_y[14]
    if landmarks_y[15] < pseudo_fix_key and landmarks_y[16] < pseudo_fix_key:
        third_up = True

    pseudo_fix_key = landmarks_y[18]
    if landmarks_y[19] < pseudo_fix_key and landmarks_y[20] < pseudo_fix_key:
        pinky_up = True

    return thumb_closer, thumb_up, index_up, second_up, third_up, pinky_up


#
# Extract counting gestures, if any is present.
#
def check_count_gestures(thumb_up, index_up, second_up, third_up, pinky_up):
    gesture = "none"
    if sum([index_up, second_up, third_up, pinky_up]) == 1 and not thumb_up:
        gesture = "one"

    if sum([index_up, second_up, third_up, pinky_up]) == 2:
        gesture = "two"

    if index_up and second_up and not (thumb_up or third_up or pinky_up):
        gesture = "peace"

    if sum([thumb_up, index_up, second_up, third_up, pinky_up]) == 3:
        gesture = "three"

    if sum([thumb_up, index_up, second_up, third_up, pinky_up]) == 4:
        gesture = "four"

    if index_up and second_up and third_up and pinky_up and thumb_up:
        gesture = "five"

    return gesture


#
# Get the most frequent gesture.
#
def most_frequent(last_gestures):
    counter = 0
    gesture = last_gestures[0]

    for i in last_gestures:
        curr_frequency = last_gestures.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            gesture = i

    if gesture == 'none':
        return ''
    else:
        return gesture


def is_reversed(keypoints):
    if keypoints[4] > keypoints[18]:
        return True
    return False


#
# If the hand is moving along the x axis for multiple times, within a specific number of frames, then the user is
# waving.
#
def get_wave_gesture(landmarks, wave_frames, last_hand_x_position, temporary_wave_gestures):
    this_hand_x_position = landmarks[8]['x']
    if abs(last_hand_x_position - this_hand_x_position) > 0.28:
        temporary_wave_gestures.append(True)
        last_hand_x_position = this_hand_x_position
    else:
        wave_frames += 1
    if len(temporary_wave_gestures) == 7:
        wave_frames = 0
        aux_frames = wave_frames
        temporary_wave_gestures = []
        if aux_frames < 20:
            return True, last_hand_x_position, temporary_wave_gestures, wave_frames

    return False, last_hand_x_position, temporary_wave_gestures, wave_frames
