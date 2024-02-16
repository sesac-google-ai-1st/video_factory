
document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/video');

    socket.on('progress_update', function (msg) {
        var progressBar = document.getElementById('progress-bar');
        var progressDesc = document.getElementById('progress-description');
        var progressText = document.getElementById('progress-text');
        var progressStep = document.getElementById('progress-step');
        progressBar.style.width = msg.progress + '%';
        progressDesc.innerHTML = msg.description;
        progressText.innerHTML = msg.progress + '%';
        progressStep.innerHTML = msg.step_now_total;

        // 생성된 이미지 URL이 있는지 확인
        if (msg.image_url) {
            // 새로운 img 엘리먼트 생성
            var imgElement = document.createElement('img');
            imgElement.classList.add('generated_image');
            imgElement.width = 350;
            imgElement.src = msg.image_url;

            // img 엘리먼트를 'image-container'에 추가
            var imageContainer = document.getElementById('image-container');
            imageContainer.appendChild(imgElement);
        }

    });
});

// const socket = io.connect("http://localhost:5000/socket.io/");
// 클라이언트 측 JavaScript
var socket = io.connect('http://' + document.domain + ':' + location.port + '/video');

socket.on('connect', function() {
    console.log('Socket.IO에 연결되었습니다.');
});

socket.on('disconnect', function() {
    console.log('Socket.IO에서 연결이 해제되었습니다.');
});

// video_generation_complete 이벤트 핸들러
socket.on('video_generation_complete', function() {
    console.log('video_generation_complete 이벤트를 수신했습니다.');
    
    // 디버그 메시지 추가
    console.log('페이지를 리다이렉트합니다.');

    // 리다이렉션 코드 (URL을 직접 지정)
    window.location.href = "/download_video";  // 또는 원하는 URL로 변경

    // 디버그 메시지 추가
    console.log('리다이렉션 이후의 메시지');
});
