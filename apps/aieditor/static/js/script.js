/**
 * 'subtopic-checkbox' class 체크박스 중 선택된 것의 name을 획득하는 함수.
 * @returns {Array} 선택된 체크박스의 names을 담은 리스트.
 */
function getCheckedCheckboxNames() {
  const checkboxes = document.querySelectorAll('.subtopic-checkbox');
  const checkedNames = [];

  checkboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      checkedNames.push(checkbox.name);
    }
  });

  return checkedNames;
}

/**
 * 선택한 subtopic을 strong 요소에 담고, 
 * 그 subtopic에 해당하는 script를 담을 textarea를 만들어서 반환하는 함수.
 * @param {Array} checkedNames - 선택된 체크박스의 names을 담은 리스트.
 * @param {number} index - script의 순서를 가리키는 인덱스. subtopic이 n개 선택된 경우, 그 중 몇번째인지 구분하는 역할.
 * @returns {HTMLTextAreaElement} 만들어진 textarea 요소.
 */
function createTextarea(checkedNames, index) {
  const scriptBoxes = document.querySelector('.script-boxes'); // 선택한 subtopic과 textarea가 표시될 부모 요소.

  const strongElement = document.createElement('strong');
  strongElement.classList.add('selected-subtopic');
  strongElement.innerHTML = document.getElementById(checkedNames[index]).innerText.substring(2).replace(/^\.+/g, '').trim(); // index번째 체크박스 name을 id로 가지는 요소의 innerText : subtopic 자체
  scriptBoxes.appendChild(strongElement);

  const textarea = document.createElement('textarea');
  textarea.classList.add('script-box');
  textarea.setAttribute("readonly", "true");  // 수정할 수 없게 설정
  textarea.setAttribute('placeholder', `${index + 1}번째 스크립트를 생성 중입니다. 조금만 기다려주세요.`);
  scriptBoxes.appendChild(textarea);
  return textarea;
}


const topicform = document.getElementById("topic-form");
const scriptform = document.getElementById("script-form");

//#region 이벤트
/**
 * 소주제 생성 버튼 클릭 이벤트 리스너.
 * chain이 stream으로 보내는 chunk를 누적하며 textarea 내에 업데이트합니다.
 */
scriptform.addEventListener("submit", async (event) => {
  event.preventDefault();

  // topicform에서 user_input을, 
  // getCheckedCheckboxNames로 선택된 체크박스의 names를 가져옵니다.
  const user_input = topicform.elements.user_input.value;
  const checkedNames = getCheckedCheckboxNames();

  let currentTextareaIndex = 0;

  // user_input, checkedNames으로 Flask server에 요청 보냅니다.
  // json형식으로 보냄
  const response = await fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user_input: user_input, button2: true, checkedNames: checkedNames }),
  });

  // 스트리밍된 response 텍스트를 디코딩하기 위해 TextDecoder를 만듭니다.
  const decoder = new TextDecoder();
  // response body 읽기 위해 ReadableStream를 만듭니다.
  const reader = response.body.getReader();

  // response stream을 누적할 chunks 변수를 정의하고, 
  // createTextarea 함수로 chunks를 담을 textarea를 만듭니다.
  let chunks = "";
  let currentTextarea = createTextarea(checkedNames, currentTextareaIndex);

  
  // response stream을 읽고 chunks에 누적하여 textarea에 추가합니다.
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    chunks += decoder.decode(value);

    if (chunks.includes("End of script")) {   // 해당 주제에 관한 스크립트 생성이 끝난 경우,
      chunks = chunks.replace("End of script", "");
      if (chunks.includes("The end")) {   // 모든 스크립트 생성이 끝난 경우, break
        chunks = chunks.replace("The end", "");
        currentTextarea.value = chunks;
        currentTextarea.removeAttribute("readonly"); // Remove readonly attribute to allow editing
        break;
      }
      currentTextarea.value = chunks;
      currentTextarea.removeAttribute("readonly"); // Remove readonly attribute to allow editing
      currentTextareaIndex++;
      currentTextarea = createTextarea(checkedNames, currentTextareaIndex);   // 다음 주제에 관한 스크립트를 넣을 textarea 생성
      chunks = "";  // Reset chunks for the new textarea
    } else {
      currentTextarea.value = chunks;
    }
  };
});
//#endregion

console.log("\n============finish==============");




// /* 프롬프트 */
// function handleInput(event) {
//     console.log("handleInput called"); // 디버깅을 위한 콘솔 로그
//     var input = event.target;
//     var sendButtonImage = document.querySelector('.prompt-send-button img');

//     if (input.value.trim() !== '') {
//         sendButtonImage.src = 'images/arrow1.png';
//     } else {
//         sendButtonImage.src = 'images/arrow2.png';
//     }
// }

// // Function to handle the script creation form submission
// function handleScriptCreation() {
//     {% for i in range(1, 11) %}
//         // Check if the checkbox for the subtopic is selected
//         if (document.getElementById('subtopic{{ i }}').checked) {
//             const subtopicIndex = {{ i }};
//             const textareaElement = document.getElementById('script{{ i }}');
//             const formData = new FormData(document.forms[1]);
//             formData.append("subtopic_index", subtopicIndex);

//             // Make a POST request to the server to generate scripts
//             fetch("/generate_scripts", {
//                 method: "POST",
//                 body: formData,
//             })
//             .then(response => response.text())
//             .then(scriptText => {
//                 // Update the textarea with the received script text
//                 textareaElement.value = scriptText;
//             });
//         }
//     {% endfor %}
// }






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

/* 소주제 체크박스 클릭시  */
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




// /* 우측 스크립트 */
// document.addEventListener('DOMContentLoaded', function() {
//     document.querySelectorAll('.subtopic-checkbox').forEach(function(checkbox, index) {
//         checkbox.addEventListener('change', function() {
//             if (this.checked) {
//                 // 선택된 소주제 제목을 우측 섹션에 표시
//                 var selectedSubtopicTitle = this.nextElementSibling.textContent;
//                 document.querySelector('.selected-subtopic').textContent = selectedSubtopicTitle;

//                 // 여기서 스크립트 박스의 내용을 업데이트하는 로직을 추가할 수 있습니다.
//                 // 예시로, 각 스크립트 박스에 '스크립트 내용 ' + 인덱스를 추가합니다.
//                 var scriptBoxes = document.querySelectorAll('.script-box');
//                 scriptBoxes.forEach(function(box, i) {
//                     box.textContent = '스크립트 내용 ' + (index + 1) + '.' + (i + 1);
//                 });
//             }
//         });
//     });
// });



// /* 슬라이드 */
// document.addEventListener("DOMContentLoaded", function() {
//     const slideshow = document.querySelector('.slide-show');
//     let scrollAmount = 0;
//     const slideWidth = 210; // 각 슬라이드의 너비 + margin
//     const slideCount = slideshow.children.length / 2; // 슬라이드 개수의 절반 (중복 제외)
//     const maxScroll = slideWidth * slideCount; // 한 세트의 슬라이드 길이

//     function slide() {
//         scrollAmount += 1; // 스크롤 속도를 절반으로 줄임
//         if (scrollAmount >= maxScroll) {
//             scrollAmount = 0; // 슬라이드 쇼를 처음으로 리셋
//         }
//         slideshow.scrollLeft = scrollAmount;

//         requestAnimationFrame(slide);
//     }

//     requestAnimationFrame(slide);
// });

// /* 비디오 영역 */
// document.addEventListener("DOMContentLoaded", function() {
//     const slider = document.querySelector('.video-slider');
//     const slideCount = slider.children.length;
//     const cardWidth = 300; // 비디오 카드의 너비 설정
//     let currentIndex = 0; // 현재 슬라이더의 위치

//     document.querySelector('.left-nav').addEventListener('click', function() {
//         if (currentIndex > 0) {
//             currentIndex--;
//             slider.style.transform = `translateX(-${currentIndex * (cardWidth + 10)}px)`;
//         }
//     });

//     document.querySelector('.right-nav').addEventListener('click', function() {
//         if (currentIndex < slideCount - 4) {
//             currentIndex++;
//             slider.style.transform = `translateX(-${currentIndex * (cardWidth + 10)}px)`;
//         }
//     });
// });

// window.addEventListener('scroll', function() {
//     var header = document.querySelector('.bottom-bg');
//     var scrollValue = window.scrollY;

//     // 초기 투명도 값 (0.8: 80% 불투명, 0: 완전 투명)
//     var initialOpacity = 0.8;
    
//     // 스크롤 값에 따라 투명도를 서서히 조절
//     var opacity = Math.min(1, scrollValue / 100); // 여기서 100은 투명도가 서서히 변화하기 시작하는 스크롤 위치입니다.
//     opacity = 1 - (1 - initialOpacity) * opacity;
    
//     header.style.opacity = opacity.toFixed(2); // 투명도 값을 소수점 둘째 자리까지로 제한
// });






// /* gpt 연결 */
// function displaySubtopics(subtopics) {
//     const container = document.querySelector('.subtopics-container');
//     container.innerHTML = ''; // 기존 내용을 지웁니다.

//     subtopics.forEach(topic => {
//         const topicDiv = document.createElement('div');
//         topicDiv.textContent = topic;
//         container.appendChild(topicDiv);
//     });
// }


// // script.js (또는 해당 스크립트가 포함된 파일)
// document.getElementById('submit-button').addEventListener('click', () => {
//     const promptText = document.querySelector('.prompt-input').value;

//     fetch('/get-subtopics', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ prompt: promptText })
//     })
//     .then(response => response.json())
//     .then(data => {
//         displaySubtopics(data.choices[0].text);
//     })
//     .catch(error => console.error('Error:', error));
// });

// function displaySubtopics(text) {
//     const container = document.querySelector('.subtopics-container');
//     container.innerHTML = text; // GPT API 응답 텍스트를 표시
// }
