const imageContainer = document.getElementById('image-container');
let totalImageCount = 0; // 서버에서 받아오는 total_image_count 값으로 갱신될 예정

function checkForNewImage(index) {
    // 이미지 확인 요청을 서버에 보냅니다.
    fetch(`/check_image/${index}`)
        .then(response => response.json())
        .then(data => {
            if (data.image_exists) {
                // 서버에서 이미지를 찾았을 때 표시합니다.
                displayImage(index);
                totalImageCount = data.total_image_count;
            } else {
                // 서버에서 이미지를 찾지 못했을 때, 일정 시간 후에 재시도합니다.
                setTimeout(() => checkForNewImage(index), 5000);
            }
        })
        .catch(error => {
            console.error(`Error checking for image ${index}:`, error);
        });
}

function displayImage(index) {
    index_str = String(index).padStart(3, '0');
    // 이미지 컨테이너에 새로운 이미지를 추가합니다.
    const imgElement = document.createElement('img');
    imgElement.classList.add('generated_image');
    imgElement.src = `/func_images/${index_str}.jpg`;
    imgElement.width = 350;
    imageContainer.appendChild(imgElement);

    // 모든 이미지가 표시되었다면
    if (index === totalImageCount) {
        console.log('All images displayed!');
    } else {
        // 다음 이미지 확인을 위해 재귀 호출
        checkForNewImage(index + 1);
    }
}

// 시작은 1번 이미지부터
checkForNewImage(1);

document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/video');

    socket.on('progress_update', function (msg) {
        var progressBar = document.getElementById('progress-bar');
        var progressText = document.getElementById('progress-text');
        progressBar.style.width = msg.progress + '%';
        progressText.innerHTML = msg.progress + '%';
    });
});

// const socket = io.connect("http://localhost:5000/socket.io/");
// 클라이언트 측 JavaScript
var socket = io.connect('http://127.0.0.1:5000/video');

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
