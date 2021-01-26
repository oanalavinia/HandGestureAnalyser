# USAGE
# python server.py

import cv2
from flask import Flask
from flask import Response
from flask import render_template
from get_gestures_from_webcam import get_gestures_from_webcam as gestures

app = Flask(__name__)


def serve_streams():
    camera = cv2.VideoCapture(0)
    yield from gestures.get_gestures(camera)
    camera.release()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(serve_streams(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run(port=80, debug=True,
            threaded=True, use_reloader=False)
