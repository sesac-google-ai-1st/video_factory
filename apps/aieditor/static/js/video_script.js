// // 이미지 생성 중일 때 표시할 프로그래스바 요소 가져오기
// const progressBarContainer = document.getElementById('progress-bar-container');
// const progressBar = document.getElementById('progress-bar');
// const progressText = document.getElementById('progress-text');

// // 이미지 생성 중인 총 갯수
// const totalImages = 100; // 총 이미지 갯수를 원하는 값으로 설정하세요

// // 현재 생성된 이미지 갯수 초기화
// let currentImageCount = 0;

// // 이미지 생성 함수
// function generateImages() {
//     // 이미지 생성 중인 동안에는 프로그래스바를 표시
//     progressBarContainer.style.display = 'block';

//     // 실제 이미지 생성 로직
//     for (let i = 0; i < totalImages; i++) {
//         // 이미지 생성 코드 작성

//         // 생성된 이미지 갯수 업데이트
//         currentImageCount++;

//         // 프로그래스바 업데이트
//         updateProgressBar();

//         // 이미지 생성 로직 추가
//     }

//     // 이미지 생성 완료 후 프로그래스바 숨기기
//     progressBarContainer.style.display = 'none';
// }

// // 프로그래스바 업데이트 함수
// function updateProgressBar() {
//     // 현재 생성된 이미지 갯수와 총 이미지 갯수로부터 진행 상태 계산
//     const progress = (currentImageCount / totalImages) * 100;

//     // 프로그래스바 업데이트
//     progressBar.style.width = `${progress}%`;
//     progressText.innerText = `${progress.toFixed(2)}%`;
// }

// // 이미지 생성 함수 호출
// generateImages();


document.addEventListener('DOMContentLoaded', function () {
    // 비동기 작업 시작
    performAsyncTask();
});

async function performAsyncTask() {
    try {
        // 비동기 작업 시작 전에 화면을 업데이트
        updateProgress(0, '작업을 시작합니다...');

        // 여기에 실제 비동기 작업 수행
        // 예: 서버에 데이터를 요청하거나 복잡한 계산 등

        for (let i = 0; i <= 100; i++) {
            // 가상의 진행 상태 업데이트
            await sleep(100); // 100ms 대기
            updateProgress(i, `진행 중... (${i}%)`);
        }

        // 비동기 작업 완료 후 마무리 작업
        updateProgress(100, '작업이 완료되었습니다.');

    } catch (error) {
        console.error('Error during async task:', error);
        updateProgress(0, '오류가 발생했습니다.');
    }
}

// 프로그래스바 및 텍스트 업데이트 함수
function updateProgress(progress, text) {
    const progressBar = document.querySelector('.progress-bar');
    const progressText = document.getElementById('progress-text');

    progressBar.style.width = `${progress}%`;
    progressText.innerText = text;
}

// 간단한 sleep 함수
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

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