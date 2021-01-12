def get_fingers(landmarks, is_reversed):
    thump_up = False
    index_up = False
    second_up = False
    third_up = False
    pinky_up = False

    pseudo_fix_key = landmarks[2]['x']
    if not is_reversed:
        if landmarks[3]['x'] < pseudo_fix_key and landmarks[4]['x'] < pseudo_fix_key:
            # print("thumb up")
            thump_up = True
    else:
        if landmarks[3]['x'] > pseudo_fix_key and landmarks[4]['x'] > pseudo_fix_key:
            # print("thumb up")
            thump_up = True

    pseudo_fix_key = landmarks[6]['y']
    if landmarks[7]['y'] < pseudo_fix_key and landmarks[8]['y'] < pseudo_fix_key:
        # print("first up")
        index_up = True

    pseudo_fix_key = landmarks[10]['y']
    if landmarks[11]['y'] < pseudo_fix_key and landmarks[12]['y'] < pseudo_fix_key:
        # print("second up")
        second_up = True

    pseudo_fix_key = landmarks[14]['y']
    if landmarks[15]['y'] < pseudo_fix_key and landmarks[16]['y'] < pseudo_fix_key:
        # print("third up")
        third_up = True

    pseudo_fix_key = landmarks[18]['y']
    if landmarks[19]['y'] < pseudo_fix_key and landmarks[20]['y'] < pseudo_fix_key:
        # print("forth up")
        pinky_up = True

    gesture = "none"

    if index_up and not second_up and not thump_up and not third_up and not pinky_up:
        gesture = "1"

    if index_up and second_up and (not thump_up and not third_up and not pinky_up):
        gesture = "2"

    if index_up and second_up and third_up and (not thump_up and not pinky_up):
        gesture = "3"

    if index_up and second_up and third_up and pinky_up and not thump_up:
        gesture = "4"

    if index_up and second_up and third_up and pinky_up and thump_up:
        gesture = "5"

    pseudo_fix_key = landmarks[2]['y']
    thumb_up_oriented = True
    if landmarks[3]['y'] < pseudo_fix_key and landmarks[4]['y'] < pseudo_fix_key:
        thumb_up_oriented = False

    # if not(thump_up and thumb_up_oriented) and (not index_up and not third_up and not pinky_up):
    #     gesture = "ok"

    # Special cases for thumbs up and down
    if landmarks[0]['x'] < landmarks[13]['x']:
        fist_closed = False
        if landmarks[6]['x'] - landmarks[5]['x'] > landmarks[8]['x'] - landmarks[5]['x'] and \
                landmarks[10]['x'] - landmarks[9]['x'] > landmarks[12]['x'] - landmarks[9]['x'] and \
                landmarks[14]['x'] - landmarks[13]['x'] > landmarks[16]['x'] - landmarks[13]['x'] and \
                landmarks[18]['x'] - landmarks[17]['x'] > landmarks[20]['x'] - landmarks[17]['x']:
            fist_closed = True
    else:
        fist_closed = False
        if landmarks[6]['x'] - landmarks[5]['x'] <= landmarks[8]['x'] - landmarks[5]['x'] and \
                landmarks[10]['x'] - landmarks[9]['x'] <= landmarks[12]['x'] - landmarks[9]['x'] and \
                landmarks[14]['x'] - landmarks[13]['x'] <= landmarks[16]['x'] - landmarks[13]['x'] and \
                landmarks[18]['x'] - landmarks[17]['x'] <= landmarks[20]['x'] - landmarks[17]['x']:
            fist_closed = True

    # The image is reversed?
    if thumb_up_oriented and fist_closed:
        gesture = "thumb down"

    if not thumb_up_oriented and fist_closed:
        gesture = "thumb up"

    # if not(thump_up and thumb_up_oriented) and (not index_up and not third_up and not pinky_up):
    #     gesture = "ok"
    #
    # if not (keypoints[17]['y'] > keypoints[5]['y'] and not thumb_up_oriented):
    #     gesture = "thumbs down"

    return gesture


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
