$(document).on('click', '#maybe_start_quiz', function() {
    var myModal = new bootstrap.Modal(document.getElementById('question_modal'));
    myModal.show();
});

$(document).on('click', '#start_question_game', function() {
    $('#question_modal').removeData();
    $('#question_modal').data('answersTime', [])
    $('#question_modal').data('quizId', Date.now())
    $('#question_modal').data('correctAnswers', [])
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
                    console.log(data)
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
//        Save time when question has startedr
        var startTime = new Date() / 1000 | 0;
        var previousTimes = $('#question_modal').data('answersTime');
        previousTimes.push(startTime)
        $('#question_modal').data('answersTime', previousTimes)
//        Save correct answer.
        var correctAnswers = $('#question_modal').data('correctAnswers');
        correctAnswers.push(questionContent.correct_answer)
        $('#question_modal').data('correctAnswers', correctAnswers)
//        Update question.
        setTimeout(function() {
            $('#question_content').text(' ');
            $('.question_container').prop('hidden', true);
            deferred.resolve();
        }, 1000);
    });
}

//var askQuestions = function(data) {
//    var deferred = $.Deferred().resolve();
//    $.each(data, function() {
//        deferred = deferred.then($.proxy(askQuestion, null, this.question));
//    });
//}

//var askQuestion = function(questionContent) {
//    var deferred = $.Deferred();
//    var d = new Date();
//    $('.question_container').prop('hidden', false);
//    $('#question_content').text(questionContent);
////    var startTime = d.getTime();
//    $.post('/questions', {'quizId': $('#question_modal').data('quizId'),'startTime': d.getTime()});
//    setTimeout(function() {
//        $('#question_content').text(' ');
//        $('.question_container').prop('hidden', true);
//        deferred.resolve();
//    }, 4000);
//    return deferred.promise();
//}