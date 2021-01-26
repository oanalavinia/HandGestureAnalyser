$(document).on('click', '#maybe_start_quiz', function() {
    var myModal = new bootstrap.Modal(document.getElementById('question_modal'));
    myModal.show();
});

$(document).on('click', '#start_question_game', function() {
    $('#question_modal').removeData();
    $('#question_modal').data('answersTime', []);
    $('#question_modal').data('quizId', Date.now());
    $('#question_modal').data('correctAnswers', []);
    $('#question_modal').data('questionsText', []);
    $.get('/questions', function(data) {
        response = JSON.parse(data);
        askQuestion(response.shift()).then(function nextQuestion() {
            if (response.length) {
                askQuestion(response.shift()).then(nextQuestion);
            } else {
                console.log($('#question_modal').data('answersTime'))
                $.post('/questions',
                {
                    'quizId': $('#question_modal').data('quizId'),
                    'answersTime': $('#question_modal').data('answersTime'),
                    'correctAnswers': $('#question_modal').data('correctAnswers')
                }).done(function(data) {
                    var questions_text = $('#question_modal').data('questionsText');
                    var actual_answers = $('#question_modal').data('correctAnswers');
                    var user_answers = JSON.parse(data).results;
                    $('#question_body').empty();
                    $.each(user_answers, function(indx) {
                        var checkedAnswers = $('<div class="answer"></div>')
                        var question = $('<span></span>').html(questions_text[indx]);
                        checkedAnswers.append(question)
                        if (actual_answers[indx] == user_answers[indx]) {
                            var answer = $('<span class="badge bg-primary"></span>').html(user_answers[indx]);
                            checkedAnswers.append(answer);
                        } else {
                            var value = user_answers[indx] ? user_answers[indx] : "Not given"
                            var answer = $('<span class="badge bg-danger"></span>').html(value);
                            checkedAnswers.append(answer);
                        }
                        $('#question_body').append(checkedAnswers);
                    });
                    var answers_modal = new bootstrap.Modal(document.getElementById('answers_modal'));
                    answers_modal.show();
                });
            }
        });
    });
});

function askQuestion(questionContent) {
    $('.question_container').prop('hidden', false);
    $('#question_content').text(questionContent.question);
    return $.Deferred(function() {
        var deferred = this;
//        Save time when question has started.
        var startTime = new Date() / 1000 | 0;
        var previousTimes = $('#question_modal').data('answersTime');
        previousTimes.push(startTime)
        $('#question_modal').data('answersTime', previousTimes)
//        Save correct answer.
        var correctAnswers = $('#question_modal').data('correctAnswers');
        correctAnswers.push(questionContent.correct_answer)
        $('#question_modal').data('correctAnswers', correctAnswers)
//        Save questions.
        var questionsText = $('#question_modal').data('questionsText');
        questionsText.push(questionContent.question)
        $('#question_modal').data('questionsText', questionsText)
//        Update question.
        setTimeout(function() {
            $('#question_content').text(' ');
            $('.question_container').prop('hidden', true);
            deferred.resolve();
        }, 10000);
    });
}