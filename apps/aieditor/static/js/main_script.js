/**
 * 버튼 클릭 시 로딩 중을 표시하는 기능
 * @type {HTMLElement} theButton - 클릭 이벤트가 연결된 버튼 요소
 * @event click - 버튼 클릭 시 발생하는 이벤트
 */
const theButton = document.querySelector(".button");

theButton.addEventListener("click", () => {
    theButton.classList.add("button--loading");
});