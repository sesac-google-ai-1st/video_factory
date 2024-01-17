from flask import Flask, render_template, stream_template
from flask import request, Response
from apps.aieditor.func.chain import ScriptAssistant

app = Flask(__name__)

subtopics = []
script_assistant_instance = None


@app.route("/", methods=["GET", "POST"])
def maintest():
    global subtopics
    global script_assistant_instance

    # 사용자 입력을 저장할 변수 초기화
    user_input = ""

    # 소주제 표시 여부를 결정하는 플래그
    display_subtopics = False

    selected_model = None

    # POST 요청 처리
    if request.method == "POST":
        print("request:", request)
        print("request.form:", request.form)

        # "소주제 표시" 버튼이 눌린 경우, request.form으로 data가 들어옴
        if "button1" in request.form:
            user_input = request.form.get("user_input")
            display_subtopics = True if user_input.strip() else False
            selected_model = request.form["modelSelect"]

            # ScriptAssistant 인스턴스 생성 또는 업데이트
            script_assistant_instance = ScriptAssistant(selected_model)

            # ScriptAssistant 인스턴스가 생성되어 있을 경우에만 make_subtopics 호출
            if script_assistant_instance:
                subtopics = script_assistant_instance.make_subtopics(user_input)
                print(subtopics)  # 한글

        # "스크립트 생성" 버튼이 눌린 경우, request.form은 비어있고, request.json으로 data가 들어오도록 함(script.js의 fetch 참고)
        if not (request.form) and request.json["button2"]:
            # 선택된 소주제에 대한 스크립트 생성
            display_subtopics = True
            user_input = request.json["user_input"]
            checkedNames = request.json["checkedNames"]
            print(checkedNames)
            # checkedNames : 선택된 체크박스의 name(subtopic{i})들을 리스트로 반환(script.js의 getCheckedCheckboxNames 참고)

            # ScriptAssistant 인스턴스가 생성되어 있을 경우에만 make_scripts 호출
            if script_assistant_instance:
                selected_idx = list(map(lambda name: int(name[8:]), checkedNames))
                print(selected_idx)
                # selected_idx : 선택한 subtopic의 인덱스 리스트, subtopic{i}의 숫자만 추출

                selected_list = script_assistant_instance.select_subtopics(selected_idx)
                print(selected_list)  # 영어 (make_scripts에 들어갈 input이라, 할당할 필요없지만 확인차 출력)

                def event_stream():
                    """스크립트 생성을 위해 server-sent event stream을 생성합니다.

                    make_scripts함수가 stream으로 str chunk를 반환합니다.
                    Gemini가 empty string을 생성하고 작동을 멈추는 경우가 있기때문에, 에러로 간주하고 종료합니다.

                    선택된 subtopic이 n개일 때 반복문을 돌며, n개의 script를 생성합니다.
                    각 script의 생성이 완료되면, "End of script"를 반환합니다.
                    모든 script 생성이 완료되면, "The end"를 반환합니다.

                    참고 코드: https://dev.to/jethrolarson/streaming-chatgpt-api-responses-with-python-and-javascript-22d0

                    Yields:
                        str: Chunks of generated scripts or error messages.
                    """
                    for i in range(len(checkedNames)):
                        for chunk in script_assistant_instance.make_scripts(
                            user_input, str(i + 1)
                        ):
                            print(chunk)
                            if chunk:
                                yield chunk
                            else:
                                yield "\n\n ⚠️ 에러가 발생했습니다! 다시 생성해주세요. ⚠️The end"
                        yield "End of script"
                    yield "The end"

                return Response(event_stream(), mimetype="text/event-stream")

    # 템플릿 스트림 렌더링. 변수들을 템플릿으로 전달
    return stream_template(
        "maintest.html",
        subtopics=subtopics,
        user_input=user_input,
        display_subtopics=display_subtopics,
    )


if __name__ == "__main__":
    app.run(debug=True)
