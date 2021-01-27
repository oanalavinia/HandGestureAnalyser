import matplotlib.pyplot as plt
from scripts import queries as qr
import io
from PIL import Image


def getGestures(start_time):
    dict = qr.queryGesturesInSession(start_time)
    plt.bar(dict.keys(), dict.values())
    plt.title('Most frequent gestures')
    plt.xlabel('gesture')
    plt.ylabel('number of frames')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    im = Image.open(buf)
    return im
