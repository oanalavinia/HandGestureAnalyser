def get_gestures(landmarks, is_reversed):
    #
    # Get fingers orientation
    #
    thumb_up, index_up, second_up, third_up, pinky_up = get_fingers_orientation(landmarks, is_reversed)

    #
    # Simple gestures
    #
    gesture = check_count_gestures(thumb_up, index_up, second_up, third_up, pinky_up)

    #
    # Get more information about hand
    #
    thumb_up_oriented, thumb_in_fist, four_fingers_closed = get_hand_info(landmarks)

    # Get more gestures.
    if thumb_in_fist and four_fingers_closed:
        gesture = "fist"

    if thumb_up_oriented and not thumb_in_fist and four_fingers_closed:
        gesture = "thumb down"

    if not thumb_up_oriented and not thumb_in_fist and four_fingers_closed:
        gesture = "thumb up"

    return gesture


def get_hand_info(landmarks):
    right_hand = True
    if landmarks[0]['x'] < landmarks[13]['x']:
        right_hand = False

    pseudo_fix_key = landmarks[2]['y']
    thumb_up_oriented = True
    if landmarks[3]['y'] < pseudo_fix_key and landmarks[4]['y'] < pseudo_fix_key:
        thumb_up_oriented = False

    thumb_in_fist = True
    if abs(landmarks[6]['y'] - landmarks[4]['y']) > 0.16:
        thumb_in_fist = False

    # We check to see if the four fingers are closed together, considering the hand used
    if not right_hand:
        four_fingers_closed = False
        if landmarks[6]['x'] - landmarks[5]['x'] > landmarks[8]['x'] - landmarks[5]['x'] and \
                landmarks[10]['x'] - landmarks[9]['x'] > landmarks[12]['x'] - landmarks[9]['x'] and \
                landmarks[14]['x'] - landmarks[13]['x'] > landmarks[16]['x'] - landmarks[13]['x'] and \
                landmarks[18]['x'] - landmarks[17]['x'] > landmarks[20]['x'] - landmarks[17]['x']:
            four_fingers_closed = True
    else:
        four_fingers_closed = False
        if landmarks[6]['x'] - landmarks[5]['x'] <= landmarks[8]['x'] - landmarks[5]['x'] and \
                landmarks[10]['x'] - landmarks[9]['x'] <= landmarks[12]['x'] - landmarks[9]['x'] and \
                landmarks[14]['x'] - landmarks[13]['x'] <= landmarks[16]['x'] - landmarks[13]['x'] and \
                landmarks[18]['x'] - landmarks[17]['x'] <= landmarks[20]['x'] - landmarks[17]['x']:
            four_fingers_closed = True

    return thumb_up_oriented, thumb_in_fist, four_fingers_closed


#
# Check which fingers are up oriented.
#
def get_fingers_orientation(landmarks, is_reversed):
    thumb_up = False
    index_up = False
    second_up = False
    third_up = False
    pinky_up = False

    pseudo_fix_key = landmarks[2]['x']
    if not is_reversed:
        if landmarks[3]['x'] < pseudo_fix_key and landmarks[4]['x'] < pseudo_fix_key:
            thumb_up = True
    else:
        if landmarks[3]['x'] > pseudo_fix_key and landmarks[4]['x'] > pseudo_fix_key:
            thumb_up = True

    pseudo_fix_key = landmarks[6]['y']
    if landmarks[7]['y'] < pseudo_fix_key and landmarks[8]['y'] < pseudo_fix_key:
        index_up = True

    pseudo_fix_key = landmarks[10]['y']
    if landmarks[11]['y'] < pseudo_fix_key and landmarks[12]['y'] < pseudo_fix_key:
        second_up = True

    pseudo_fix_key = landmarks[14]['y']
    if landmarks[15]['y'] < pseudo_fix_key and landmarks[16]['y'] < pseudo_fix_key:
        third_up = True

    pseudo_fix_key = landmarks[18]['y']
    if landmarks[19]['y'] < pseudo_fix_key and landmarks[20]['y'] < pseudo_fix_key:
        pinky_up = True

    return thumb_up, index_up, second_up, third_up, pinky_up


#
# Extract counting gestures, if any is present.
#
def check_count_gestures(thumb_up, index_up, second_up, third_up, pinky_up):
    gesture = "none"
    if sum([index_up, second_up, third_up, pinky_up]) == 1 and not thumb_up:
        gesture = "1"

    if sum([thumb_up, index_up, second_up, third_up, pinky_up]) == 2:
        gesture = "2"

    if index_up and second_up and not (thumb_up or third_up or pinky_up):
        gesture = "2 / peace"

    if sum([thumb_up, index_up, second_up, third_up, pinky_up]) == 3:
        gesture = "3"

    if sum([thumb_up, index_up, second_up, third_up, pinky_up]) == 4:
        gesture = "4"

    if index_up and second_up and third_up and pinky_up and thumb_up:
        gesture = "5 / paper"

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
    if keypoints[4]['x'] > keypoints[18]['x']:
        return True
    return False


#
# If the hand is moving along the x axis for multiple times, within a specific number of frames, then the user is
# waving.
#
def get_wave_gesture(landmarks, wave_frames, last_hand_x_position, temporary_wave_gestures):
    this_hand_x_position = landmarks[8]['x']
    if abs(last_hand_x_position - this_hand_x_position) > 0.18:
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
