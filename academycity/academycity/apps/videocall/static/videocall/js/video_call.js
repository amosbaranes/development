// Frontend io we have { io.on as input, io.emit as op)
let width = 250;
let height = 250;

var canvas = document.querySelector('#idCanvas');
var profileImage = document.querySelector('#idImage');
var takePicButton = document.querySelector('#idTakePictureBtn');
//--
var myVideoArea = document.querySelector('#idMyVideoTag');
var user_id = document.getElementById("user_id").value.toString()
var user_call_id = user_id + "_" + Math.floor(Math.random()*1000000000)
console.log('user_call_id=', user_call_id);
var myStream;
//--
getCameras();
//--

var theirVideoArea;
var allVideos = document.querySelector('#idAllVideos');
var allVideosArray = {}


var myName = document.querySelector('#idMyName');
var myMessage = document.querySelector('#idMessage');
var sendMessage = document.querySelector('#idSendMessage');
var chatArea = document.querySelector('#idChatArea');
var ROOM = "chat";
var SIGNAL_ROOM = 'SIGNAL_ROOM';

var websocketProtocol;
console.log('redishost=', redishost);
console.log('host = ', window.location.host);
console.log('protocol=', location.protocol);
if (location.protocol === 'http:') {
    websocketProtocol = 'ws';
} else {
    websocketProtocol = 'wss';
}
var websocketBaseUrl = websocketProtocol + '://' + window.location.host + '/ws/';
console.log(websocketBaseUrl)

// using test stun server
var configuration = {
    'iceServers': [{
        'url': 'stun:stun1.l.google.com:19302' //'stun:stun.l.google.com:19302'
    }]
};

var signalingArea = document.querySelector('#idSignalingArea');

takePicButton.addEventListener('click', function () {
    console.log('take picture');
    takeProfilePic();
});

startStream()

// WebSocket -> .send, .onmessage, .onclose


const videoSignalSocket = new WebSocket(
    websocketBaseUrl + 'video_call/signal/'
);

var allPeersConn = {}
var rtcPeerConn;
videoSignalSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if(allPeersConn[data.user_call_id] == null)
    {
      rtcPeerConn = null
    }
    else {
      rtcPeerConn = allPeersConn[data.user_call_id]
      theirVideoArea = allVideosArray[data.user_call_id]
    }
    displaySignalMessage('Signal received:' + data.type);

    // setup RTC peer connection object
    if (!rtcPeerConn) {
        console.log('rtc Peer conn doesnt exists yet');
        startSignaling(rtcId = data.user_call_id);
    }

    // we are sending some bogus signal on load with type='user_here'. we call below
    // code only for real signal message
    if (data.type != 'user_here') {
        console.log('data type != user_here');
        var message = JSON.parse(data.message); // parse json from message

        // sdp message means remote party made us an offer
        if (message.sdp) {
            rtcPeerConn.setRemoteDescription(
                new RTCSessionDescription(message.sdp), function () {
                    // if we received an offer, we need to answer
                    if (rtcPeerConn.remoteDescription.type == 'offer') {
                        rtcPeerConn.createAnswer(sendLocalDesc, logError);
                    }
                }, logError);
        } else {
            rtcPeerConn.addIceCandidate(new RTCIceCandidate(message.candidate));
        }
    }
};

videoSignalSocket.onclose = function (e) {
    console.error('video signal socket closed unexpectedly');
};

// send ready state signal
// this one also should only be told to other user, not both user
var videoSignalSocketReady = setInterval(function () {
    // keep checking if socket is ready at certain intervals
    // once ready, send a signal and exit loop
    console.log('ready state=', videoSignalSocket.readyState);
    if (videoSignalSocket.readyState === 1) {
        videoSignalSocket.send(JSON.stringify({
            'type': 'user_here',
            'message': 'Are you ready for a call?',
            'room': SIGNAL_ROOM,
            'user_call_id': user_call_id
        }));
        clearInterval(videoSignalSocketReady);
    }
}, 1000);

function displaySignalMessage(message) {
    signalingArea.innerHTML = signalingArea.innerHTML + "<br/>" + message;
}

function startSignaling(rtcId) {
    console.log('startSignaling');
    displaySignalMessage('starting signaling...');
    rtcPeerConn = new RTCPeerConnection(configuration);
    allPeersConn[rtcId] = rtcPeerConn
    video = document.createElement("video");
    video.autoplay = true
    video.id = "id_" + rtcId
    video.width="240"
    video.height="240"
    theirVideoArea = video
    allVideos.appendChild(video);
    allVideosArray[rtcId] = video
    console.log(allVideos.outerHTML)

    // send any ice candidates to other peer
    rtcPeerConn.onicecandidate = function (evt) {
        if (evt.candidate) {
            videoSignalSocket.send(JSON.stringify({
                'type': 'ice candidate',
                'message': JSON.stringify({
                    'candidate': evt.candidate
                }),
                'room': SIGNAL_ROOM,
                'user_call_id': user_call_id
            }));
        }
        displaySignalMessage('completed that ice candidate...');
    }

    // when we receive an offer, we return our offer
    // let the 'negotiationneeded' event trigger offer generation
    rtcPeerConn.onnegotiationneeded = function () {
        displaySignalMessage(' on negotiation called');
        rtcPeerConn.createOffer(sendLocalDesc, logError);
    }
    // once remote stream arrives, show it in remote video element
    rtcPeerConn.onaddstream = function (evt) {
        displaySignalMessage('going to add their stream...');
        theirVideoArea.srcObject = evt.stream;
    }

    // get a local stream, show it in our video tag and add it to be sent
    // startStream();
    rtcPeerConn.addStream(myStream); // this triggers event our peer needs to get our stream
}

function sendLocalDesc(desc) {
    console.log('desc' + desc);
    rtcPeerConn.setLocalDescription(desc, function () {
        displaySignalMessage('sending local description');
        videoSignalSocket.send(JSON.stringify({
            'type': 'SDP',
            'message': JSON.stringify({
                'sdp': rtcPeerConn.localDescription
            }),
            'room': SIGNAL_ROOM,
            'user_call_id': user_call_id
        }));
    }, logError);
}

function logError(error) {
    displaySignalMessage(error.name + ':' + error.message);
}

function takeProfilePic() {
    var context = canvas.getContext('2d');
    canvas.width = width;
    canvas.height = height;
    context.drawImage(myVideoArea, 0, 0, width, height);
    var data = canvas.toDataURL('image/png');
    profileImage.setAttribute('src', data);
}


// new
function startStream() {
  if (navigator.mediaDevices.getUserMedia) {
    console.log('startStream');
    let constraints = {
        video: {width: 1280, height: 720},
        audio: true
    };
    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        console.log('Stream connected successfully');
        myVideoArea.srcObject = stream;
        myStream = stream
    }).catch(function (error) {
        console.log('error in stream:', error);
    });
  }
}

function getCameras() {

    if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
        console.log("enumerateDevices() not supported.");
        return;
    }

    // List cameras and microphones.
    navigator.mediaDevices.enumerateDevices()
        .then(function (devices) {
            devices.forEach(function (device) {
                console.log(device.kind + ": " + device.label +
                    " id = " + device.deviceId);

                // add different camera options to a select tag

                if (device.kind === 'videoinput') {
                    var cameraSelect = document.querySelector('#camera');
                    let option = document.createElement('option');
                    option.value = device.deviceId;
                    option.text = device.label;
                    cameraSelect.append(option);
                } else if (device.kind === 'audioinput')
                {
                    var inputAudio = document.querySelector('#audioinput');
                    let option = document.createElement('option');
                    option.value = device.deviceId;
                    option.text = device.label;
                    inputAudio.append(option);

                } else if (device.kind === 'audiooutput')
                {
                    var outputAudio = document.querySelector('#audiooutput');
                    let option = document.createElement('option');
                    option.value = device.deviceId;
                    option.text = device.label;
                    outputAudio.append(option);
                }
            }
            );
        })
        .catch(function (err) {
            console.log(err.name + ": " + err.message);
        });
}