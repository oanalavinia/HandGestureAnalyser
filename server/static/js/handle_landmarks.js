$(document).ready(function() {
    // Our input frames will come from here.
    const videoElement = document.getElementsByClassName('input_video')[0];
    const canvasElement = document.getElementsByClassName('output_canvas')[0];
    const controlsElement = document.getElementsByClassName('control-panel')[0];
    const canvasCtx = canvasElement.getContext('2d');
    canvasCtx.font = "bold 30px Arial";
    canvasCtx.fillStyle = "blue";
    const fpsControl = new FPS();

    // Optimization: Turn off animated spinner after its hiding animation is done.
    const spinner = document.querySelector('.loading');
    spinner.ontransitionend = () => {
      spinner.style.display = 'none';
    };

    function onResults(results) {
      // Hide the spinner.
      document.body.classList.add('loaded');

      // Update the frame rate.
      fpsControl.tick();

      // Draw the overlays.
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(
          results.image, 0, 0, canvasElement.width, canvasElement.height);
      if (results.multiHandLandmarks && results.multiHandedness) {
        for (let index = 0; index < results.multiHandLandmarks.length; index++) {
          const classification = results.multiHandedness[index];
          const isRightHand = classification.label === 'Right';
          const landmarks = results.multiHandLandmarks[index];

          var data = {'landmarks': landmarks};
          landmarks_x = []
          landmarks_y = []
          for (index in landmarks) {
            landmarks_x.push(landmarks[index]['x'])
            landmarks_y.push(landmarks[index]['y'])
          }

          $.post('/get_gesture',
          {
            'landmarks_x': landmarks_x,
            'landmarks_y': landmarks_y
          }).done(function(data) {
            var result = JSON.parse(data);
            var gesture = result.gesture;
            var context = result.context;
            if (gesture && gesture != 'none') {
                console.log(gesture)
                drawGesture(gesture);
//                canvasCtx.fillText(gesture, 10, 25);
                // If we are in the image context, it may be needed, depending on the gesture,
                // to zoom in or zoom out on the image.
                if (context == 'Image') {
                    maybeZoom(gesture);
                }
                if (context == 'PDFDocument') {
                    maybeChangePage(gesture);
                }
            } else {
//                canvasCtx.fillText("No gesture detected", 10, 25);
            }
          });

          drawConnectors(
              canvasCtx, landmarks, HAND_CONNECTIONS,
              {color: isRightHand ? '#00FF00' : '#FF0000'}),
          drawLandmarks(canvasCtx, landmarks, {
            color: isRightHand ? '#00FF00' : '#FF0000',
            fillColor: isRightHand ? '#FF0000' : '#00FF00',
            radius: (x) => {
              return lerp(x.from.z, -0.15, .1, 10, 1);
            }
          });
        }
      }
      canvasCtx.restore();
    }

    const hands = new Hands({locateFile: (file) => {
      return `https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.1/${file}`;
    }});
    hands.onResults(onResults);

    /**
     * Instantiate a camera. We'll feed each frame we receive into the solution.
     */
    const camera = new Camera(videoElement, {
      onFrame: async () => {
        await hands.send({image: videoElement});
      },
      width: 1080,
      height: 650
    });
    camera.start();

    // Present a control panel through which the user can manipulate the solution
    // options.
    new ControlPanel(controlsElement, {
      selfieMode: true,
      maxNumHands: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    })
    .add([
      new StaticText({title: 'MediaPipe Hands'}),
      fpsControl,
      new Toggle({title: 'Selfie Mode', field: 'selfieMode'}),
      new Slider({
        title: 'Min Detection Confidence',
        field: 'minDetectionConfidence',
        range: [0, 1],
        step: 0.01
      }),
      new Slider({
        title: 'Min Tracking Confidence',
        field: 'minTrackingConfidence',
        range: [0, 1],
        step: 0.01
      }),
    ])
    .on(options => {
      videoElement.classList.toggle('selfie', options.selfieMode);
      hands.setOptions(options);
    });
});

var lastNoneTime = Date.now() / 1000.0;
var timeout;
var drawGesture = function(gesture, ctx) {
    if (gesture && gesture != 'none') {
        clearTimeout(timeout);
        //canvasCtx.fillText(gesture, 10, 25);
        $('#thisGesture').html(getGestureName(gesture));
//        lastNoneTime = Date.now();
        timeout = setTimeout(function() {
            $('#thisGesture').html("");
        }, 1000)
    }
//    else {
//        lastNoneTime = Date.now() / 1000.0;
//
//        if (Date.now() / 1000.0 - lastNoneTime > 1) {
//            $('#thisGesture').html("No gesture detected");
//        }
//    }
};

var getGestureName = function(gesture) {
    if (gesture == "one") {
        return "One Finger Detected";
    } else if(gesture == "two") {
        return "Two Fingers Detected";
    } else if(gesture == "three") {
        return "Three Fingers Detected";
    } else if(gesture == "four") {
        return "Four Fingers Detected";
    } else if(gesture == "five") {
        return "Five Fingers Detected";
    } else if(gesture == "thumbsUp") {
        return "Thumbs Up Detected";
    } else if(gesture == "thumbsDown") {
        return "Thumbs Down Detected";
    } else if(gesture == "zoomOut") {
        return "Zoom Out";
    } else if(gesture == "zoomIn") {
        return "Zoom In";
    }
    return "";
};