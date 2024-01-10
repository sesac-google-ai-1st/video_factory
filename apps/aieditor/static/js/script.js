

/* 프롬프트 */
function handleInput(event) {
    console.log("handleInput called"); // 디버깅을 위한 콘솔 로그
    var input = event.target;
    var sendButtonImage = document.querySelector('.prompt-send-button img');

    if (input.value.trim() !== '') {
        sendButtonImage.src = 'images/arrow1.png';
    } else {
        sendButtonImage.src = 'images/arrow2.png';
    }
}

// /* 소주제 */
// document.addEventListener('DOMContentLoaded', function() {
//     document.querySelectorAll('.subtopic-checkbox').forEach(function(checkbox) {
//         checkbox.addEventListener('change', function() {
//             console.log('체크박스 상태 변경됨: ' + this.checked);
//             // 여기에서 추가적인 로직을 구현할 수 있습니다.
//         });
//     });

//     document.querySelectorAll('.subtopic-refresh-button').forEach(function(button) {
//         button.addEventListener('click', function() {
//             alert('새로고침 기능이 실행됩니다.');
//             // 여기에서 새로고침 로직을 구현할 수 있습니다.
//         });
//     });
// });

// /* 소주제 체크박스 클릭시  */
// document.addEventListener('DOMContentLoaded', function() {
//     let checkboxes = document.querySelectorAll('.subtopic-checkbox');

//     checkboxes.forEach(function(checkbox) {
//         checkbox.addEventListener('change', function() {
//             // 모든 체크박스의 선택을 해제
//             checkboxes.forEach(function(otherCheckbox) {
//                 if (otherCheckbox !== checkbox) {
//                     otherCheckbox.checked = false;
//                 }
//             });
            
//         });
//     });
// });




/* 우측 스크립트 */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.subtopic-checkbox').forEach(function(checkbox, index) {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                // 선택된 소주제 제목을 우측 섹션에 표시
                var selectedSubtopicTitle = this.nextElementSibling.textContent;
                document.querySelector('.selected-subtopic').textContent = selectedSubtopicTitle;

                // 여기서 스크립트 박스의 내용을 업데이트하는 로직을 추가할 수 있습니다.
                // 예시로, 각 스크립트 박스에 '스크립트 내용 ' + 인덱스를 추가합니다.
                var scriptBoxes = document.querySelectorAll('.script-box');
                scriptBoxes.forEach(function(box, i) {
                    box.textContent = '스크립트 내용 ' + (index + 1) + '.' + (i + 1);
                });
            }
        });
    });
});



/* 슬라이드 */
document.addEventListener("DOMContentLoaded", function() {
    const slideshow = document.querySelector('.slide-show');
    let scrollAmount = 0;
    const slideWidth = 210; // 각 슬라이드의 너비 + margin
    const slideCount = slideshow.children.length / 2; // 슬라이드 개수의 절반 (중복 제외)
    const maxScroll = slideWidth * slideCount; // 한 세트의 슬라이드 길이

    function slide() {
        scrollAmount += 1; // 스크롤 속도를 절반으로 줄임
        if (scrollAmount >= maxScroll) {
            scrollAmount = 0; // 슬라이드 쇼를 처음으로 리셋
        }
        slideshow.scrollLeft = scrollAmount;

        requestAnimationFrame(slide);
    }

    requestAnimationFrame(slide);
});

/* 비디오 영역 */
document.addEventListener("DOMContentLoaded", function() {
    const slider = document.querySelector('.video-slider');
    const slideCount = slider.children.length;
    const cardWidth = 300; // 비디오 카드의 너비 설정
    let currentIndex = 0; // 현재 슬라이더의 위치

    document.querySelector('.left-nav').addEventListener('click', function() {
        if (currentIndex > 0) {
            currentIndex--;
            slider.style.transform = `translateX(-${currentIndex * (cardWidth + 10)}px)`;
        }
    });

    document.querySelector('.right-nav').addEventListener('click', function() {
        if (currentIndex < slideCount - 4) {
            currentIndex++;
            slider.style.transform = `translateX(-${currentIndex * (cardWidth + 10)}px)`;
        }
    });
});

window.addEventListener('scroll', function() {
    var header = document.querySelector('.bottom-bg');
    var scrollValue = window.scrollY;

    // 초기 투명도 값 (0.8: 80% 불투명, 0: 완전 투명)
    var initialOpacity = 0.8;
    
    // 스크롤 값에 따라 투명도를 서서히 조절
    var opacity = Math.min(1, scrollValue / 100); // 여기서 100은 투명도가 서서히 변화하기 시작하는 스크롤 위치입니다.
    opacity = 1 - (1 - initialOpacity) * opacity;
    
    header.style.opacity = opacity.toFixed(2); // 투명도 값을 소수점 둘째 자리까지로 제한
});






/* gpt 연결 */
function displaySubtopics(subtopics) {
    const container = document.querySelector('.subtopics-container');
    container.innerHTML = ''; // 기존 내용을 지웁니다.

    subtopics.forEach(topic => {
        const topicDiv = document.createElement('div');
        topicDiv.textContent = topic;
        container.appendChild(topicDiv);
    });
}


// script.js (또는 해당 스크립트가 포함된 파일)
document.getElementById('submit-button').addEventListener('click', () => {
    const promptText = document.querySelector('.prompt-input').value;

    fetch('/get-subtopics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: promptText })
    })
    .then(response => response.json())
    .then(data => {
        displaySubtopics(data.choices[0].text);
    })
    .catch(error => console.error('Error:', error));
});

function displaySubtopics(text) {
    const container = document.querySelector('.subtopics-container');
    container.innerHTML = text; // GPT API 응답 텍스트를 표시
}
