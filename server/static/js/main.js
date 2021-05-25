$(document).on('click', '#get_info_button', function() {
    var myModal = new bootstrap.Modal(document.getElementById('get_info'));
    myModal.show();
});

//
// Working with images.
//
$(document).on('click', '#work_with_images', function() {
    $('#images_game').removeAttr('hidden');
});

$(document).on('click', '#go_back', function(evt) {
    $('#images_game').prop("hidden", !this.checked);
    $('#go_back').prop("hidden", !this.checked);
    $('#uploaded_image_content').prop("hidden", !this.checked);
    $('.output_canvas').removeClass('fix_canvas');
    $('.output_canvas').attr('width', '1080px');
    $('.output_canvas').attr('height', '650px');
});

var applyZoom = function(widthRatio, heightRatio) {
    //    Get image info.
    var canvas = $('#uploaded_image_canvas');
    var fileUrl = canvas.attr('fileUrl');
    var width = canvas.attr('fileWidth');
    var height = canvas.attr('fileHeight');

    //    Do the zoom on the original image.
    fetch(fileUrl).then(function(response) {
      return response.blob();
    }).then(function(myBlob) {
        canvas.attr('width', width);
        canvas.attr('height', height);
        var ctx = canvas[0].getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        var img = new Image();

        img.onload = function() {
            var newWidth = width * widthRatio;
            var newHeight = height * heightRatio;
            ctx.drawImage(img, 0, 0, newWidth, newHeight);
            canvas.attr('fileWidth', newWidth);
            canvas.attr('fileHeight', newHeight);
        }
        img.src = URL.createObjectURL(myBlob);
    });
};

$(document).on('click', '#zoomOut', function(evt) {
    applyZoom(1.1, 1.1);
    $.post({
        url: '/add_image_rule',
        data: {gesture: 'zoomOut'},
        success: function(data) {
            console.log(data);
        }
    });
});

$(document).on('click', '#zoomIn', function(evt) {
    applyZoom(0.9, 0.9);
    $.post({
        url: '/add_image_rule',
        data: {gesture: 'zoomIn'},
        success: function(data) {
            console.log(data);
        }
    });
});

// When a file is submitted upload it to the server. On success display it on canvas.
// Also, save info about the image.
$(document).on('click', '#submit_image', function(event) {
    event.preventDefault();
    var input = $('#input_image').get(0).files[0];
    var fd = new FormData();
    fd.append( 'file', input);
    fd.append( 'context', "Image");

    $.ajax({
      url: '/uploader',
      data: fd,
      processData: false,
      contentType: false,
      type: 'POST',
      success: function(data) {
        // Set-up the display.
        $('.output_canvas').addClass('fix_canvas');
        $('.output_canvas').attr('width', '500');
        $('.output_canvas').attr('height', '350');
        $('#uploaded_image_content').removeAttr('hidden');
        $('#go_back').removeAttr('hidden');

        // Add image info.
        var fileUrl ='/static/files/' + data.fileName;
        $('#uploaded_image').attr('src', fileUrl);

        fetch(fileUrl).then(function(response) {
          return response.blob();
        }).then(function(myBlob) {
            var canvas = $('#uploaded_image_canvas');
            canvas.attr('width', data.width);
            canvas.attr('height', data.height);
            canvas.attr('fileUrl', fileUrl);
            canvas.attr('fileWidth', data.width);
            canvas.attr('fileHeight', data.height);
            var ctx = canvas[0].getContext('2d');
            var img = new Image();

            img.onload = function() {
              ctx.drawImage(img, 0, 0, data.width, data.height)
            }
            img.src = URL.createObjectURL(myBlob);
        });
      }
    });
});

var lastGestures = {};
var maybeZoom = function(gesture) {
    if (lastGestures[gesture] == undefined) {
        lastGestures[gesture] = 1;
    } else {
        lastGestures[gesture]++;
    }
    if (gesture == 'zoomOut') {
        lastGestures = {};
        applyZoom(0.9, 0.9);
        $.post({
            url: '/add_image_rule',
            data: {gesture: 'zoomOut'},
            success: function(data) {
                console.log(data);
            }
        });
    } else if (gesture == 'zoomIn') {
        lastGestures = {};
        applyZoom(1.1, 1.1);
        $.post({
            url: '/add_image_rule',
            data: {gesture: 'zoomIn'},
            success: function(data) {
                console.log(data);
            }
        });
    }
};

//
// Quiz game.
//
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

// Close camera data recording.
$(document).on('click', '#close_camera_button', function() {
    $('#close_camera_modal').data('is_camera_closed', true);
    $.post('/do_close_camera', {'do_close_camera': true}).done(function() {
        $('#open_camera_button').prop('hidden', false);
        $('#maybe_start_quiz')[0].setAttribute('aria-disabled', true);
        $('#maybe_start_quiz').addClass('disabled');
    });
});

// Open camera data recording.
$(document).on('click', '#open_camera_button', function() {
    $('#close_camera_modal').data('is_camera_closed', false);
    $.post('/do_close_camera', {'do_close_camera': false}).done(function() {
        $('#open_camera_button').prop('hidden', true);
        $('#maybe_start_quiz')[0].setAttribute('aria-disabled', false);
        $('#maybe_start_quiz').removeClass('disabled');
    });
});

$(document).on('keypress',function(e) {
    if(e.which == 115) {
        $.post('/save_data').done(function() {
            console.log("Data saved.");
        });
    }
    if(e.which == 116) {
        $.post('/save_gesture_start_time', {'start_time': Date.now()}).done(function() {
            console.log("Gesture started time saved.");
        });
    }
});