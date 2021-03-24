$(document).ready(function(){
    let namespace = "/test";
    let video = document.querySelector("#videoElement");
    let canvas = document.querySelector("#canvasElement");
    let ctx = canvas.getContext('2d');
    photo = document.getElementById('photo');
    var localMediaStream = null;
    canvas.width = 640;
    canvas.height = 480;
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    function sendSnapshot() {
      if (!localMediaStream) {
        return;
      }

      ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 640, 480);

      let dataURL = canvas.toDataURL('image/jpeg');
      socket.emit('input image', dataURL);

      socket.emit('output image')

//      var img = new Image();
//      socket.on('out-image-event',function(data){
//          img.src = dataURL//data.image_data
//          photo.setAttribute('src', data.image_data);
//      });
    }

    socket.on('connect', function() {
      console.log('Connected!');
    });

    var constraints = {
      video: {
        width: { min: 640 },
        height: { min: 480 }
      }
    };

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
      video.srcObject = stream;
      localMediaStream = stream;

      setInterval(function () {
        sendSnapshot();
      }, 250);
    }).catch(function(error) {
      console.log(error);
    });
});

$(document).on('click', '#maybe_start_quiz', function() {
    var myModal = new bootstrap.Modal(document.getElementById('question_modal'));
    myModal.show();
});

$(document).on('click', '#get_info_button', function() {
    var myModal = new bootstrap.Modal(document.getElementById('get_info'));
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

//setInterval(function() {
//    if ($('#close_camera_modal').data('is_camera_closed') == false) {
//        $.get('/check_wave').done(function(data) {
//            console.log(JSON.parse(data));
//            if(JSON.parse(data).closeCamera) {
//                var myModal = new bootstrap.Modal(document.getElementById('close_camera_modal'));
//                myModal.show();
//            }
//        });
//    }
//}, 10000)

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