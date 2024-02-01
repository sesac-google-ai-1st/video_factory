// 이미지 생성 중일 때 표시할 프로그래스바 요소 가져오기
const progressBarContainer = document.getElementById('progress-bar-container');
const progressBar = document.getElementById('progress-bar');
const progressText = document.getElementById('progress-text');


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
    // 이미지 컨테이너에 새로운 이미지를 추가합니다.
    const imgElement = document.createElement('img');
    imgElement.classList.add('generated_image');
    imgElement.src = `/func_images/${index}.jpg`;
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