# USAGE
# python server.py

import logging
import os
from camera import Camera
from flask_socketio import SocketIO, emit
from engineio.payload import Payload

from sys import stdout
from flask import Flask
from flask import Response
from flask import render_template
from flask import request, session, send_file
from werkzeug.utils import secure_filename
import json
from io import BytesIO
from datetime import datetime
from get_gestures_from_webcam import get_gestures_from_webcam as gestures
from scripts import questions as qs
from scripts import queries as qr
from scripts import statistics as st
from PIL import Image

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = '/home/oanalavinia/Documents/Master/WADe/Disertatie/HandGestureAnalyser/server/static/files'
Payload.max_decode_packets = 500
socketio = SocketIO(app)
camera = Camera()
quiz = qs.QuizGame(camera.get_gesture_obj())

app.secret_key = '5b7373780e35434090c87dc4c9d15a2d'


@socketio.on('input image', namespace='/test')
def test_message(input):
    input = input.split(",")[1]
    camera.enqueue_input(input)


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")


def gen():
    """Video streaming generator function."""

    app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame()  # pil_image_to_base64(camera.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tostring() + b'\r\n')


@app.route("/")
def index():
    session['startTime'] = datetime.now()
    return render_template("index.html")


@app.route("/statistics")
def statistics():
    binary_image = st.getGestures(session['startTime'])
    img_io = BytesIO()
    rgb_im = binary_image.convert('RGB')
    rgb_im.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(
        img_io,
        mimetype='image/jpeg',
        as_attachment=False,
        attachment_filename='statistics.jpeg')


@app.route("/video_feed")
def video_feed():
    recording_start_time = datetime.now()
    return Response(gen(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/current_gesture", methods=['GET'])
def current_gesture():
    return json.dumps({'gesture': camera.get_gesture()})


@app.route("/get_gesture", methods=['POST'])
def get_gesture():
    landmarks_x = request.form.getlist("landmarks_x[]")
    landmarks_y = request.form.getlist("landmarks_y[]")
    landmarks_x = [float(x) for x in landmarks_x]
    landmarks_y = [float(y) for y in landmarks_y]
    if landmarks_x:
        gesture = camera.get_gesture_obj().get_gesture_from_landmarks(landmarks_x, landmarks_y)
        return json.dumps({'gesture': gesture})
    return json.dumps({'gesture': "none"})


@app.route("/questions", methods=['GET', 'POST'])
def questions():
    # gestures.save_data()
    if request.method == 'GET':
        camera.get_gesture_obj().set_context("QuizGame")
        return quiz.create_question_game()
    else:
        # gestures.save_data()
        user_answers = quiz.get_correct_answers(request.form.getlist('answersTime[]'))
        return json.dumps({'status': 'OK', 'results': user_answers})


# @app.route('/check_wave')
# def check_wave():
#     gestures.save_data()
#     close_camera = qr.check_close_camera(datetime.now())
#     return json.dumps({'closeCamera': close_camera})

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # f.save(secure_filename(f.filename))
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        width, height = image.size
        print(width, height)

        return {'fileName':file.filename, 'width':width, 'height':height}


@app.route('/do_close_camera', methods=['POST'])
def do_close_camera():
    print("do close {}".format(request.form.get('do_close_camera')))
    if request.form.get('do_close_camera') == "true":
        gestures.set_record(False)
    elif request.form.get('do_close_camera') == "false":
        gestures.set_record(True)

    return json.dumps({'response': "ok"})


if __name__ == '__main__':
    # app.run(port=80, debug=True,
    #         threaded=True, use_reloader=False)
    socketio.run(app, host="0.0.0.0", port="5000", debug=True, use_reloader=False, ssl_context='adhoc')
