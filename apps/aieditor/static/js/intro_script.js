// use cases

function playVideo(videoCard) {
    var video = videoCard.querySelector('video');
    if (video.paused) {
        video.play();
    } else {
        video.pause();
    }
}

function playVideo(videoCard) {
    var videoSrc = videoCard.querySelector('video source').src;
    var modalVideo = document.getElementById('modalVideo');
    var videoModal = document.getElementById('videoModal');

    // 모달 내 비디오 소스 설정 및 재생
    modalVideo.src = videoSrc;
    videoModal.style.display = "flex"; // 모달 표시
    modalVideo.play(); // 비디오 재생

    // 모달 닫기 버튼 이벤트
    var closeModalButton = videoModal.querySelector('.close-modal');
    closeModalButton.onclick = function() {
        videoModal.style.display = "none"; // 모달 숨김
        modalVideo.pause(); // 비디오 일시 정지
        modalVideo.currentTime = 0; // 비디오 시간 초기화
        modalVideo.src = ""; // 소스 제거
    };
}


function closeModal() {
    var videoModal = document.getElementById('videoModal');
    var modalVideo = document.getElementById('modalVideo');

    videoModal.style.display = "none"; // 모달 숨김
    modalVideo.pause(); // 비디오 일시 정지
    modalVideo.currentTime = 0; // 비디오 시간 초기화
    modalVideo.src = ""; // 소스 제거
}

// 배경 클릭 이벤트 추가
window.onclick = function(event) {
    var videoModal = document.getElementById('videoModal');
    if (event.target == videoModal) {
        closeModal();
    }
}

// teams
function resizeBox(element) {
    // Reset the size of all team members
    document.querySelectorAll('.team-member').forEach(function(box) {
        box.style.width = '240px';
    });
    // Expand the hovered team member
    element.style.width = '720px';
}

function resetBoxSize() {
    document.querySelectorAll('.team-member').forEach(function(box) {
        box.style.width = '360px';
    });
}
