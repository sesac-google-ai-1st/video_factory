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
 * bgm 확인용 창 띄우기
 * checkFile로 서버에 BGM 파일이 생성되었는지 확인하고, 생성되었다면 팝업 창을 띄움.
 * @param {HTMLElement} button - 클릭된 bgm 버튼 요소
 */
const bgmButton = document.getElementById('bgm-button');

// bgm 버튼이 클릭되면 처리할 함수
bgmButton.addEventListener("click", (event) => {
  event.preventDefault(); 
  console.log("BGM 버튼 클릭");
  checkFile();    // bgm 파일이 생성되었는지 check
});

// bgm check 함수
function checkFile() {
  var user_input = document.getElementById('user_input').getAttribute('value');
  var filePath = `static/audio/musicgen_${user_input}.wav`;
  // 파일 존재 여부 확인
  fetch(filePath, { method: 'GET' })
      .then(response => {
          if (response.ok) {
            bgmButton.classList.remove('button--loading');
            document.getElementById('music_player').src = filePath;
            openBgmModal();
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


function openBgmModal() {
  const modal = document.querySelector('.modal');  // 모달의 클래스 선택자로 변경
  const audio = document.querySelector('audio');  // audio 태그를 찾아 변수에 할당
  if (audio) {
    audio.volume = 0.5;   // 기본 볼륨 0.5로 설정
  }
  modal.style.display = 'flex';  // modal 변수의 css 스타일 중 display 속성을 flex로 변경 
}

function closeBgmModal(event) {
  event.preventDefault();
  const modal = document.querySelector('.modal');  // 모달의 클래스 선택자로 변경
  const audio = document.querySelector('audio');  // audio 태그를 찾아 변수에 할당
  if (audio) {
    audio.pause();   // modal 닫을 때 오디오 멈추기
    audio.currentTime = 0;    // 오디오 시작지점으로 바꾸기
  }
  modal.style.display = 'none';  // modal 변수의 display 속성을 none으로 변경, 모달 안보이도록 감추기
}

// 모달 외부 클릭 시 닫기
// 모달이 2개이기 때문에 각각 할당해서 처리
document.addEventListener('DOMContentLoaded', function() {
  const modal1 = document.querySelector('.modal');  // bgm 모달을 modal1에 할당
  const modal2 = document.querySelector('.videomodal');  // image model option 모달을 modal2에 할당

  window.onclick = function(event) {  // 클릭 이벤트 발생 시 실행할 함수
    if (event.target === modal1) {    // 클릭 이벤트 발생한 곳이 modal1일 때
      closeBgmModal(event, modal1);   // bgm modal 닫기
    } else if (event.target === modal2) {    // 클릭 이벤트 발생한 곳이 modal2일 때
      closeSelectedModal(event, modal2);   // selected modal 닫기
    }
  };
});

// bgm 사용할지 말지 flask로 전달
function useornotBgm(radio) {
  const selectedValue = radio.value;  // radio값을 받아와서 selectedValue에 저장

  fetch("/script", {
      // method를 POST로 지정, 서버에 데이터 전달
      method: "POST",
      // 요청 header에 json 데이터 전송
      headers: {
          "Content-Type": "application/json",
      },
      // selectedValue 값을 JSON 형식으로 변환하여 처리
      body: JSON.stringify({ backgroundmusic: selectedValue }),
  })
  .then(response => {   // 응답이 처리되지 않았을 때
      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }
  })
  .catch(error => {
      console.error("Fetch error:", error);
  });
}


/**
 * image model 선택 창 띄우기
 * @param {HTMLElement} button - 클릭된 <영상 만들기> 버튼 요소
 */
const SelectedButton = document.getElementById('selected-button');

SelectedButton.addEventListener("click", (event) => {
  event.preventDefault(); 
  console.log("영상 만들기 버튼 클릭");
  openSelectedModal();
});

function openSelectedModal() {
  const videomodal = document.querySelector('.videomodal');  // 모달의 클래스 선택자로 변경
  videomodal.style.display = 'flex';
}

function closeSelectedModal(event) {
  event.preventDefault();
  const videomodal = document.querySelector('.videomodal');  // 모달의 클래스 선택자로 변경
  videomodal.style.display = 'none';
}

function imageModel(modelRadio) {
  const selectedValue = modelRadio.value;

  // Send the selected value to the Flask app using fetch
  fetch("/script", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ imageModel: selectedValue }),
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }
      // Handle the response if needed
  })
  .catch(error => {
      console.error("Fetch error:", error);
      // Handle the error if needed
  });
}

document.addEventListener('DOMContentLoaded', function () {
  const subtitleCheckbox = document.getElementById('subtitle');

  // 페이지 로딩 시 초기 이미지 업데이트
  updateImage();

  // 초기 체크박스 상태
  let isChecked = subtitleCheckbox.checked;

  // 체크박스 상태가 변경될 때마다 이미지 업데이트
  subtitleCheckbox.addEventListener('change', updateImage);
  // 체크박스 상태가 변경될 때마다 업데이트
  subtitleCheckbox.addEventListener('change', function(){
    isChecked = subtitleCheckbox.checked;
    // 서버로 데이터 전송
    sendCheckboxState(isChecked);
  });
});

// 자막 선택 체크박스 전송
function sendCheckboxState(isChecked){
  fetch("/script", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ isChecked: isChecked }),
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
})
.catch(error => {
    console.error("Fetch error:", error);
});
}

// subtitle이 선택됨에 따라 이미지 변경
function updateImage() {
  // stable, dalle 이미지와 subtitle checkbox에 각각 변수 할당
  const imageStable = document.getElementById('imageStable');
  const imageDalle = document.getElementById('imageDalle');
  const subtitleCheckbox = document.getElementById('subtitle');

  if (subtitleCheckbox.checked) {
      // 자막 체크된 경우 이미지
      imageStable.src = "/static/image/stable_sub.jpg";
      imageDalle.src = "/static/image/dalle_sub.jpg";
  } else {
      // 자막 체크가 해제된 경우 이미지
      imageStable.src = "/static/image/stableDiffusion.jpg";
      imageDalle.src = "/static/image/dalle.jpg";
  }
}

// model 선택 시 이미지만 클릭해도 radio가 선택될 수 있도록 함
function selectImage(radioButtonId) {
  const radioButton = document.getElementById(radioButtonId);
  radioButton.checked = true;
  imageModel(radioButton);
}

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
        currentTextarea.value = chunks + "●";
      }
    };
  } catch (error) {
    console.error("Fetch error:", error);
    // 여기에 적절한 오류 처리 로직 추가
    theButton.classList.remove('button--loading');
  }
});
//#endregion


//#region 이벤트
/**
 * 비디오 폼에서 "영상 만들기" 버튼 클릭 시 이벤트 핸들러.
 * 모든 textarea의 innerValue를 읽어서 배열에 저장한 후, Flask 서버에 요청을 보냄.
 * @param {Event} event - 폼 제출 이벤트
 */
const videoButton = document.getElementById("video-button");

videoButton.addEventListener("click", async (event) => {
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
//#endregion