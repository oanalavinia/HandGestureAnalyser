from pytrivia import Category, Diffculty, Type, Trivia
import json
import datetime
from scripts import queries as qrs


def create_question_game():
    my_api = Trivia(True)
    response = my_api.request(3, Category.General, Diffculty.Easy, Type.True_False)

    return json.dumps(response['results'])


def get_correct_answers(answer_timestamps):
    answers = []
    for indx, answer_timestamp in enumerate(answer_timestamps):
        # We don't consider the first 2 seconds.
        answer_time = datetime.datetime.fromtimestamp(int(answer_timestamp)) + datetime.timedelta(0, 2)
        end_answer_time = answer_time + datetime.timedelta(0, 10)
        answer = qrs.query_answers(answer_time, end_answer_time)
        answers.append(bool_from_gesture(answer))
    return answers


def bool_from_gesture(gesture):
    if gesture == "thumbsUp":
        return "True"
    elif gesture == "thumbsDown":
        return "False"
    else:
        return None
