from flask import Flask, render_template
from flask import request, Response, url_for, redirect, session
from apps.aieditor.func.chain import ScriptAssistant

app = Flask(__name__)

# session 사용을 위해 secret key를 설정
app.config["SECRET_KEY"] = "2hghg2GHgJ22H"

main_topics = []
subtopics = []
script_assistant_instance = None


@app.route("/", methods=["GET", "POST"])
def main():
    global main_topics
    global script_assistant_instance

    # 사용자 입력을 저장할 변수 초기화
    user_input = ""

    # subtopic-form을 보여줄지 여부를 저장하는 변수
    show_subtopic_form = False

    selected_model = None

    # POST 요청 처리
    if request.method == "POST":
        print("request:", request)
        print("request.form:", request.form)
        if request.form:
            user_input = request.form.get("user_input")
            selected_model = request.form["modelSelect"]

            # "주제" 버튼이 눌린 경우
            if "main-button" in request.form:
                # ScriptAssistant 인스턴스 생성 또는 업데이트
                script_assistant_instance = ScriptAssistant(selected_model)

                # ScriptAssistant 인스턴스가 생성되어 있을 경우에만 make_subtopics 호출
                if script_assistant_instance:
                    main_topics = script_assistant_instance.make_maintopic(user_input)
                    ### ~~~로딩 중~~~
                    show_subtopic_form = True

            # "대본 상세 구성하기"이 클릭된 경우
            elif "sub-button" in request.form:
                selected_maintopic = request.form.get("maintopic")

                if script_assistant_instance:
                    subtopics = script_assistant_instance.make_subtopics(
                        user_input, selected_maintopic
                    )
                    ### ~~~로딩 중~~~
                    print(subtopics)

                    # session에 데이터 저장
                    session["user_input"] = user_input
                    session["selected_model"] = selected_model  ###
                    session["selected_maintopic"] = selected_maintopic
                    session["subtopics"] = subtopics

                    # subtopic.html 페이지로 리다이렉트
                    return redirect(url_for("subtopic"))

    return render_template(
        "main.html",
        main_topics=main_topics,
        show_subtopic_form=show_subtopic_form,
        user_input=user_input,
        selected_model=selected_model,
    )


@app.route("/subtopic", methods=["GET", "POST"])
def subtopic():
    user_input = session.get("user_input", "")
    selected_model = session.get("selected_model", "")  ###
    selected_maintopic = session.get("selected_maintopic", "")
    subtopics = session.get("subtopics", "")

    # POST 요청 처리
    if request.method == "POST":
        print("request:", request)
        print("request.form:", request.form)
        print("request.json:", request.json)

        # "스크립트 생성" 버튼이 눌린 경우, request.json으로 data가 들어옴(script.js의 fetch 참고)
        if request.json["script_button"]:
            # 선택된 소주제에 대한 스크립트 생성
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
                    Gemini가 empty string을 생성하고 작동을 멈추는 경우가 있기 때문에, 에러로 간주하고 종료합니다.

                    선택된 subtopic이 n개일 때 반복문을 돌며, n개의 script를 생성합니다.
                    각 script의 생성이 완료되면, "End of script"를 반환합니다.
                    모든 script 생성이 완료되면, "The end"를 반환합니다.

                    참고 코드: https://dev.to/jethrolarson/streaming-chatgpt-api-responses-with-python-and-javascript-22d0

                    Yields:
                        str: Chunks of generated scripts or error messages.
                    """
                    try:
                        for i in range(len(checkedNames)):
                            for chunk in script_assistant_instance.make_scripts(
                                user_input, str(i + 1)
                            ):
                                print(chunk)
                                if chunk:
                                    yield chunk
                                else:
                                    # Gemini가 empty string을 생성하고 작동을 멈추는 경우가 있기 때문에, 에러를 발생시킴
                                    raise Exception("⚠️ 에러가 발생했습니다! 다시 생성해주세요. ⚠️")
                            yield "End of script"
                        yield "The end"
                    except Exception as e:
                        # 디버깅을 위해 exception 로깅
                        print(f"Error: {e}")
                        # client로 에러 메세지 전송
                        yield "Error occurred: " + str(e)

                return Response(event_stream(), mimetype="text/event-stream")

    # 템플릿 렌더링. 변수들을 템플릿으로 전달
    return render_template(
        "subtopic.html",
        user_input=user_input,
        selected_model=selected_model,  ###
        selected_maintopic=selected_maintopic,
        subtopics=subtopics,
    )


if __name__ == "__main__":
    app.run(debug=True)
