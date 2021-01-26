from pytrivia import Category, Diffculty, Type, Trivia
import json
import datetime
from scripts import queries as qrs


def use_script():
    create_question_game()


def create_question_game():
    my_api = Trivia(True)
    response = my_api.request(3, Category.General, Diffculty.Easy, Type.True_False)

    return json.dumps(response['results'])


def check_answers(user_answers, correct_answers):
    after_corecting = []
    for indx, user_answer in enumerate(user_answers):
        if (user_answer == 'thumbsUp' and user_answers[indx] is True) or (
                user_answer == 'thumbsDown' and user_answers[indx] is False):
            after_corecting.append(True)
        else:
            after_corecting.append(False)
    return after_corecting


def get_correct_answers(answer_timestamps):
    answers = []
    for indx, answer_timestamp in enumerate(answer_timestamps):
        answer_time = datetime.datetime.fromtimestamp(int(answer_timestamp))
        end_answer_time = answer_time + datetime.timedelta(0, 4)
        # print("start: {} end: {}".format(answer_time, end_answer_time))
        answer = qrs.query_answers(answer_time, end_answer_time)
        answers.append(answer)
    return answers


use_script()
