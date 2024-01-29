/**
 * 'subtopic-checkbox' 체크박스 중 선택된 것의 name을 획득하는 함수.
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
 * script-box-container를 위로 이동시키는 함수
 * @param {HTMLElement} button - 클릭된 버튼 요소
 */
function moveUp(button) {
  var container = button.parentNode;
  var previous = container.previousElementSibling;
  if (previous && previous.classList.contains("script-box-container")) {
    container.parentNode.insertBefore(container, previous);
  }
}

/**
 * script-box-container를 아래로 이동시키는 함수
 * @param {HTMLElement} button - 클릭된 버튼 요소
 */
function moveDown(button) {
  var container = button.parentNode;
  var next = container.nextElementSibling;
  if (next && next.classList.contains("script-box-container")) {
    container.parentNode.insertBefore(next, container);
  }
}

/**
 * script-box-container를 삭제하는 함수
 * @param {HTMLElement} button - 클릭된 버튼 요소
 */
function deleteScriptBox(button) {
  var container = button.parentNode;
  container.parentNode.removeChild(container);
}

/**
 * 선택한 subtopic을 strong 요소에 담고, 
 * 그 subtopic에 해당하는 script를 담을 textarea를 만들어서 반환하는 함수.
 * script-box-container의 위 아래 순서를 바꾸거나, 삭제하는 버튼을 추가하였습니다.
 * @param {Array} checkedNames - 선택된 체크박스의 names을 담은 리스트.
 * @param {number} index - script의 순서를 가리키는 인덱스. subtopic이 n개 선택된 경우, 그 중 몇번째인지 구분하는 역할.
 * @returns {HTMLTextAreaElement} 만들어진 textarea 요소.
 */
function createTextarea(checkedNames, index) {
  const scriptBoxes = document.querySelector('.script-boxes'); // 선택한 subtopic과 textarea가 표시될 부모 요소.

  const divElement = document.createElement('div');
  divElement.classList.add('script-box-container');
  scriptBoxes.appendChild(divElement);

  const strongElement = document.createElement('strong');
  strongElement.classList.add('selected-subtopic');
  strongElement.innerHTML = document.getElementById(checkedNames[index]).innerText.substring(2).replace(/^\.+/g, '').trim(); // index번째 체크박스 name을 id로 가지는 요소의 innerText : subtopic 자체
  divElement.appendChild(strongElement);

  const deleteButton = document.createElement("button");
  deleteButton.classList.add('float-right');
  deleteButton.innerHTML = "❌";
  deleteButton.onclick = function() { deleteScriptBox(this); };
  divElement.appendChild(deleteButton);

  const moveDownButton  = document.createElement("button");
  moveDownButton.classList.add('float-right');
  moveDownButton.innerHTML = "🠗";
  moveDownButton.onclick = function() { moveDown(this); };
  divElement.appendChild(moveDownButton);

  const moveUpButton = document.createElement("button");
  moveUpButton.classList.add('float-right');
  moveUpButton.innerHTML = "🠕";
  moveUpButton.onclick = function() { moveUp(this); };
  divElement.appendChild(moveUpButton);

  const textarea = document.createElement('textarea');
  textarea.classList.add('script-box');
  textarea.setAttribute("readonly", "true");  // 수정할 수 없게 설정
  textarea.setAttribute('placeholder', `${index + 1}번째 스크립트를 생성 중입니다. 생성이 끝난 후 스크립트를 수정할 수 있습니다. 조금만 기다려주세요.`);
  divElement.appendChild(textarea);
  return textarea;
}

/**
 * 버튼 클릭 시 로딩 중을 표시하는 기능
 * @type {HTMLElement} theButton - 클릭 이벤트가 연결된 버튼 요소
 * @event click - 버튼 클릭 시 발생하는 이벤트
 */
const theButton = document.querySelector(".button");

theButton.addEventListener("click", () => {
    theButton.classList.add("button--loading");
});

/**
 * bgm 확인용 창 띄우기
 * @param {HTMLElement} button - 클릭된 버튼 요소
 */
const bgmButton = document.getElementById('bgm-button');

function checkFile() {
  
  var user_input = document.getElementById('user_input').innerText;
  var filePath = `static/audio/musicgen_${user_input}.wav`;
  // 파일 존재 여부 확인
  fetch(filePath, { method: 'GET' })
      .then(response => {
          if (response.ok) {
              // 파일이 존재하면 원하는 작업 실행
              fetch("/script", {
                method: "POST",
                headers: {
                  'Content-Type': "application/json"
                },
                body: JSON.stringify({})
              })
                .then(() => {
                  bgmButton.classList.remove('button--loading');
                  openModal();
                });
              
          } else {
              // 파일이 아직 생성되지 않았으면 재귀적으로 계속 확인
              setTimeout(checkFile, 15000);  // 15초마다 확인
          }
      })
      .catch(error => {
          // 에러 발생 시 처리
          console.error('Error checking file:', error);
      });
}

bgmButton.addEventListener("click", (event) => {
  event.preventDefault();  // 기본 동작 중지
  console.log("BGM 버튼 클릭");

  checkFile();
 // 인자를 넘기지 않도록 수정
});

function openModal() {
  const modal = document.querySelector('.modal');  // 모달의 클래스 선택자로 변경
  modal.style.display = 'flex';
}

function closeModal(event) {
  event.preventDefault();
  const modal = document.querySelector('.modal');  // 모달의 클래스 선택자로 변경
  modal.style.display = 'none';
}

// 모달 외부 클릭 시 닫기
window.onclick = function(event) {
  const modal = document.querySelector('.modal');  // 모달의 클래스 선택자로 변경
  if (event.target === modal) {
    closeModal(event);
  }
};



/**
 * 비디오 폼에서 "영상 만들기" 버튼 클릭 시 이벤트 핸들러.
 * 모든 textarea의 innerValue를 읽어서 배열에 저장한 후, Flask 서버에 요청을 보냄.
 * @param {Event} event - 폼 제출 이벤트
 */
const videoForm = document.getElementById("video-form");

videoForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  // 모든 textarea의 innerValue를 읽어서 배열에 저장
  const scriptBoxes = document.querySelectorAll('.script-box');
  const scriptData = Array.from(scriptBoxes).map(textarea => textarea.value);

  // video_button과 scriptData를 JSON 형식으로 Flask server에 요청을 보냄
  try {
    const response = await fetch("/script", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ video_button: true, scriptData: scriptData }),
    });

    // 요청에 대한 응답이 실패한 경우
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    console.log("최종 스크립트 session에 저장 완료");

    // 이후 필요한 동작 수행
    // 예를 들면, 페이지를 리다이렉트하거나 다른 작업을 수행
    window.location.href = "/video";
  } catch (error) {
    console.error("Fetch error:", error);
    // 여기에 적절한 오류 처리 로직 추가
  }
});



//#region 이벤트
/**
 * 스크립트 생성 버튼 클릭 이벤트 리스너.
 * chain이 stream으로 보내는 chunk를 누적하며 textarea 내에 업데이트합니다.
 */
const scriptform = document.getElementById("script-form");

scriptform.addEventListener("submit", async (event) => {
  event.preventDefault();

  // getCheckedCheckboxNames 함수로 선택된 체크박스의 names를 가져옵니다.
  const checkedNames = getCheckedCheckboxNames();

  let currentTextareaIndex = 0;

  // script_button과 checkedNames을 json형식으로 Flask server에 요청 보냅니다.
  try {
    const response = await fetch("/script", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ script_button: true, checkedNames: checkedNames }),
    });

    // 요청에 대한 응답이 실패한 경우
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // 스트리밍된 response 텍스트를 디코딩하기 위해 TextDecoder를 만듭니다.
    const decoder = new TextDecoder();
    // response body 읽기 위해 ReadableStream를 만듭니다.
    const reader = response.body.getReader();

    // response stream을 디코딩할 chunk 변수와 누적할 chunks 변수를 정의하고, 
    // createTextarea 함수로 chunks를 담을 textarea를 만듭니다.
    let chunk = "";
    let chunks = "";
    let currentTextarea = createTextarea(checkedNames, currentTextareaIndex);

    
    // response stream을 읽고 chunks에 누적하여 textarea에 추가합니다.
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      chunk = decoder.decode(value);

      if (chunk.includes("Error:")) {
        // 서버에서 에러 메시지가 전송된 경우, alert으로 표시
        chunk = chunk.replace("Error:", "");
        currentTextarea.removeAttribute("readonly"); // Remove readonly attribute to allow editing
        theButton.classList.remove('button--loading');
        alert(chunk.trim());
        break;
      }

      chunks += chunk;

      if (chunks.includes("End of script")) {   // 해당 주제에 관한 스크립트 생성이 끝난 경우,
        chunks = chunks.replace("End of script", "");
        if (chunks.includes("The end")) {   // 모든 스크립트 생성이 끝난 경우, break
          chunks = chunks.replace("The end", "");
          currentTextarea.value = chunks;
          currentTextarea.removeAttribute("readonly"); // Remove readonly attribute to allow editing
          theButton.classList.remove('button--loading');
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
  } catch (error) {
    console.error("Fetch error:", error);
    // 여기에 적절한 오류 처리 로직 추가
    theButton.classList.remove('button--loading');
  }
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
