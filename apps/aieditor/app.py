from flask import Flask, render_template, request, url_for
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

    # 체크박스 상태를 저장하는 딕셔너리
    checkbox_states = {}

    # 체크박스로 선택된 스크립트를 저장할 리스트
    selected_scripts = [0] * 10

    selected_model = None

    # POST 요청 처리
    if request.method == "POST":
        # "소주제 표시" 버튼이 눌렸는지 확인
        if "button1" in request.form:
            user_input = request.form.get("user_input")
            display_subtopics = True if user_input.strip() else False
            selected_model = request.form["modelSelect"]

            # ScriptAssistant 인스턴스 생성 또는 업데이트
            script_assistant_instance = ScriptAssistant(selected_model)

            # ScriptAssistant 인스턴스가 생성되어 있을 경우에만 make_subtopics 호출
            if script_assistant_instance:
                subtopics = script_assistant_instance.make_subtopics(user_input)
                print(subtopics)

        # "스크립트 생성" 버튼이 눌린 경우
        if "button2" in request.form:
            # 선택된 소주제에 대한 스크립트 생성
            display_subtopics = True
            user_input = request.form.get("user_input")

            # ScriptAssistant 인스턴스가 생성되어 있을 경우에만 dd 호출
            if script_assistant_instance:
                selected_idx = [
                    i for i in range(1, 11) if request.form.get(f"subtopic{i}")
                ]
                print(selected_idx)
                selected_list = script_assistant_instance.select_subtopics(selected_idx)
                print(selected_list)

                for i, idx in enumerate(selected_idx):
                    script = script_assistant_instance.make_scripts(
                        user_input, selected_list, str(i + 1)
                    )
                    # selected_scripts.append(script)
                    selected_scripts[idx - 1] = script
                print(selected_scripts)

        # 체크박스 상태를 업데이트
        checkbox_states = {
            f"subtopic{i}": "checked" if request.form.get(f"subtopic{i}") else ""
            for i in range(1, 11)
        }

    # 템플릿 렌더링. 변수들을 템플릿으로 전달
    return render_template(
        "maintest.html",
        subtopics=subtopics,
        user_input=user_input,
        display_subtopics=display_subtopics,
        checkbox_states=checkbox_states,
        selected_scripts=selected_scripts,
    )


if __name__ == "__main__":
    app.run(debug=True)
