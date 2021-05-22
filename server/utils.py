from PIL import Image
from io import BytesIO
import io
from imageio import imread
import base64
import owlready2 as owl
from datetime import datetime


def pil_image_to_base64(image):
    pil_image = Image.fromarray(image)
    buf = BytesIO()
    pil_image.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue())


def base64_to_pil_image(base64_img):
    return Image.open(BytesIO(base64.b64decode(base64_img)))


def to_cv2(data):
    # b64_bytes = base64.b64encode(data)
    # b64_string = b64_bytes.decode()

    # reconstruct image as an numpy array
    img = imread(io.BytesIO(base64.b64decode(data)))
    return img

    # finally convert RGB image to BGR for opencv
    # and save result
    # cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


def create_rdf_instances(gesture, user):
    gest = get_gesture_instance(gesture)
    if gest:
        gest.hasGestureTime.append(datetime.now())
        gest.hasGestureName.append(gesture)
        user.makesGesture.append(gest)
    return gest


def get_gesture_instance(gesture):
    if gesture == 'wave':
        return owl.Wave()
    elif gesture == 'thumbsUp':
        return owl.ThumbsUp()
    elif gesture == 'thumbsDown':
        return owl.ThumbsDown()
    elif gesture == 'one':
        return owl.One()
    elif gesture == 'two':
        return owl.Two()
    elif gesture == 'peace':
        return owl.Peace()
    elif gesture == 'three':
        return owl.Three()
    elif gesture == 'four':
        return owl.Four()
    elif gesture == 'five':
        return owl.Five()
    elif gesture == 'fist':
        return owl.Fist()
    else:
        return None