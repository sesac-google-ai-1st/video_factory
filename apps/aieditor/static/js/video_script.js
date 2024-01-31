// 이미지 생성 중일 때 표시할 프로그래스바 요소 가져오기
const progressBarContainer = document.getElementById('progress-bar-container');
const progressBar = document.getElementById('progress-bar');
const progressText = document.getElementById('progress-text');

// 이미지 생성 중인 총 갯수
const totalImages = 100; // 총 이미지 갯수를 원하는 값으로 설정하세요

// 현재 생성된 이미지 갯수 초기화
let currentImageCount = 0;

// 이미지 생성 함수
function generateImages() {
    // 이미지 생성 중인 동안에는 프로그래스바를 표시
    progressBarContainer.style.display = 'block';

    // 실제 이미지 생성 로직
    for (let i = 0; i < totalImages; i++) {
        // 이미지 생성 코드 작성

        // 생성된 이미지 갯수 업데이트
        currentImageCount++;

        // 프로그래스바 업데이트
        updateProgressBar();

        // 이미지 생성 로직 추가
    }

    // 이미지 생성 완료 후 프로그래스바 숨기기
    progressBarContainer.style.display = 'none';
}

// 프로그래스바 업데이트 함수
function updateProgressBar() {
    // 현재 생성된 이미지 갯수와 총 이미지 갯수로부터 진행 상태 계산
    const progress = (currentImageCount / totalImages) * 100;

    // 프로그래스바 업데이트
    progressBar.style.width = `${progress}%`;
    progressText.innerText = `${progress.toFixed(2)}%`;
}

// 이미지 생성 함수 호출
generateImages();