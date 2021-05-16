# USAGE
# python server.py

import logging
import os
from camera import Camera
from flask_socketio import SocketIO
from engineio.payload import Payload

from sys import stdout
from flask import Flask
from flask import Response
from flask import render_template
from flask import request, session, send_file
from werkzeug.utils import secure_filename
import json
import pdfplumber
from io import BytesIO
from datetime import datetime
from get_gestures_from_webcam import get_gestures_from_webcam as gestures
from scripts import questions as qs
from scripts import statistics as st
from scripts import movies as mv
from PIL import Image

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config[
    'UPLOAD_FOLDER'] = '/home/oanalavinia/Documents/Master/WADe/Disertatie/HandGestureAnalyser/server/static/files'
Payload.max_decode_packets = 500
socketio = SocketIO(app)
camera = Camera()
quiz = qs.QuizGame(camera.get_gesture_obj())
movie = mv.Movie(camera.get_gesture_obj())

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
        context = camera.get_gesture_obj().get_context()
        return json.dumps({'gesture': gesture, 'context': context})
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


@app.route("/random_movies", methods=['GET'])
def random_movies():
    if request.method == 'GET':
        camera.get_gesture_obj().set_context("Marks")
        result = movie.get_rec_system().get_random_movies()
        return json.dumps({'movies': result[0], 'movie_ids': result[1]})


@app.route("/rec_movies", methods=['POST'])
def rec_movies():
    if request.method == 'POST':
        start_time = datetime.fromtimestamp(int(request.form.get('startTime')) / 1000.0)
        end_time = datetime.fromtimestamp(int(request.form.get('endTime')) / 1000.0)
        movie_ids = request.form.getlist('movie_ids[]')
        # Get gesture based on startTime and endTime.
        gesture = movie.queries_handler.query_movies(start_time, end_time)
        # gesture = "paper"
        # Get recommendation.
        rec_movies = movie.get_recommendations(gesture, movie_ids)
        print(rec_movies)

        return json.dumps({'status': 'OK', 'movies': rec_movies})
        # Add rule to owl.
        # return json.dumps({'movies': rc.get_random_movies()})


# @app.route('/check_wave')
# def check_wave():
#     gestures.save_data()
#     close_camera = qr.check_close_camera(datetime.now())
#     return json.dumps({'closeCamera': close_camera})

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        context = request.form.get('context')
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if context == "Image":
            camera.get_gesture_obj().set_context("Image")
            image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            width, height = image.size
            print(width, height)

            return {'fileName': file.filename, 'width': width, 'height': height}
        elif context == "PDFDocument":
            camera.get_gesture_obj().set_context("PDFDocument")
            with pdfplumber.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as pdf:
                page_1 = pdf.pages[0]
                nr_pages = len(pdf.pages)

            return {'fileName': file.filename, 'width': str(page_1.width), 'height': str(page_1.height),
                    'nr_pages': str(nr_pages)}


@app.route('/add_image_rule', methods=['POST'])
def add_image_rule():
    gesture = request.form.get('gesture')
    gesture_obj = camera.get_gesture_obj()
    gesture_obj.get_owl_utilities().get_contexted_rule("Image", gesture, gesture_obj.get_owl_context())

    return {'response': "done"}


@app.route('/add_file_rule', methods=['POST'])
def add_file_rule():
    gesture = request.form.get('gesture')
    gesture_obj = camera.get_gesture_obj()
    gesture_obj.get_owl_utilities().get_contexted_rule("PDFDocument", gesture, gesture_obj.get_owl_context())

    return {'response': "done"}


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
