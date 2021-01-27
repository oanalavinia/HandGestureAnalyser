# USAGE
# python server.py

import cv2
import json
import logging
from camera import Camera
from flask import Flask
from flask import Response
from flask import render_template
from flask import request
from flask_socketio import SocketIO, emit

from sys import stdout
from get_gestures_from_webcam import get_gestures_from_webcam as gestures
from scripts import questions as qs

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)
camera = Camera()

@socketio.on('input image', namespace='/test')
def test_message(input):
    input = input.split(",")[1]
    camera.enqueue_input(input)
    image_data = input # Do your magical Image processing here!!
    #image_data = image_data.decode("utf-8")
    image_data = "data:image/jpeg;base64," + image_data
    print("OUTPUT " + image_data)
    emit('out-image-event', {'image_data': image_data}, namespace='/test')
    #camera.enqueue_input(base64_to_pil_image(input))


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")

@app.route("/")
def index():
    return render_template("index.html")

def gen():
    """Video streaming generator function."""

    app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(gen(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/questions", methods=['GET', 'POST'])
def questions():
    if request.method == 'GET':
        return qs.create_question_game()
    else:
        gestures.save_data()
        print(request.form.get('answersTime'))
        # qs.get_answers(request.form.getlist('answersTime[]'))
        answers = qs.get_correct_answers(request.form.getlist('answersTime[]'))
        print(answers)
        return json.dumps({'status': 'OK', 'answers': answers})


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port="80", debug=True, use_reloader=False, ssl_context='adhoc')
