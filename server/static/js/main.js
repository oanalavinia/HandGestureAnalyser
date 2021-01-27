$(document).ready(function(){
    let namespace = "/test";
    let video = document.querySelector("#videoElement");
    let canvas = document.querySelector("#canvasElement");
    let ctx = canvas.getContext('2d');
    photo = document.getElementById('photo');
    var localMediaStream = null;
  
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  
    function sendSnapshot() {
      if (!localMediaStream) {
        return;
      }
  
      ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);
  
      let dataURL = canvas.toDataURL('image/jpeg');
      socket.emit('input image', dataURL);
  
      socket.emit('output image')
  
      var img = new Image();
      socket.on('out-image-event',function(data){
  
  
      img.src = dataURL//data.image_data
      photo.setAttribute('src', data.image_data);
  
      });
  
  
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
      }, 50);
    }).catch(function(error) {
      console.log(error);
    });
  });

$(document).on('click', '#maybe_start_quiz', function() {
    var myModal = new bootstrap.Modal(document.getElementById('question_modal'));
    myModal.show();
});

$(document).on('click', '#start_question_game', function() {
    $('#question_modal').removeData();
    $('#question_modal').data('answersTime', [])
    $('#question_modal').data('quizId', Date.now())
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
                    'answersTime': $('#question_modal').data('answersTime')
                }, function(data) {
                    console.log(data);
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
        var startTime = new Date() / 1000 | 0;
        var previousTimes = $('#question_modal').data('answersTime');
        previousTimes.push(startTime)
        $('#question_modal').data('answersTime', previousTimes)
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