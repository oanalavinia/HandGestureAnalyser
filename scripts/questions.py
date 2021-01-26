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


def get_answers_times(answerTimes):
    for answerTime in answerTimes:
        print(int(answerTime))
        print(datetime.datetime.fromtimestamp(int(answerTime)))


def get_correct_answers(answer_timestamps):
    for answer_timestamp in answer_timestamps:
        answer_time = datetime.datetime.fromtimestamp(int(answer_timestamp))
        end_answer_time = answer_time + datetime.timedelta(0, 4)
        print("start: {} end: {}".format(answer_time, end_answer_time))
        qrs.query_answers(answer_time, end_answer_time)



use_script()
