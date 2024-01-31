import os
from flask import Flask, render_template
from flask import request, Response, url_for, redirect, session, flash
from apps.aieditor.func.chain import ScriptAssistant
from apps.aieditor.func.split_script import ScriptSplitter
import threading
from apps.aieditor.func.music_gen import musicGen
import os
from apps.aieditor.func.tts_gan import voice_gan_wavenet
from apps.aieditor.func.video_edit import add_static_image_to_video
from apps.aieditor.func.img_gan import img_gan_prompt, img_gan_dalle3

app = Flask(__name__)

# session 사용을 위해 secret key를 설정
app.config["SECRET_KEY"] = "2hghg2GHgJ22H"

# openai api key 이건 삭제하고 업로드
api_key = ""

imgPath = os.path.join("static", "image")
app.config["IMAGE_FOLDER"] = imgPath

main_topics = []
subtopics = []
script_assistant_instance = None
music_gen_instance = musicGen()
background_music_option = "no"


@app.route("/merge", methods=["GET", "POST"])
def merge():
    # message = ""
    global api_key
    maintheme = "폼페이의 마지막 날"
    scripts = [
        "베수비오 화산이 폭발하던 그 순간, 폼페이는 어땠을까요? \
                오늘 우리는 그 끔찍한 순간을 들여다봅니다. \
                화산재와 용암으로 하늘이 뒤덮였고, 폼페이 사람들은 어떻게 반응했을까요? \
                자, 이제 그들의 용기와 우리에게 전하는 메시지, 자연재해 앞에서 우리의 대처 방법을 함께 탐색해봅시다."
    ]
    splits = ScriptSplitter()

    if request.method == "POST":
        print("request : ", request)
        print("request.form :", request.form)

        # 스크립트 나눠서 리스트에 담기
        split_text = splits.split_script2sentences(scripts)
        print(split_text)

        # 이미지 생성용 프롬프트 만들기
        prompts = img_gan_prompt(maintheme, split_text)
        print(prompts)

        # 더빙 음성 만들기
        voice_gan_wavenet(split_text)

        # 이미지 생성
        img_gan_dalle3(api_key, prompts)

        # def add_static_image_to_video(image_path, audio_path, clip_path, output_path):
        image_path = (
            "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/images/"
        )
        audio_path = (
            "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/voice/"
        )
        clip_path = (
            "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/clip/"
        )
        output_path = (
            "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/finalclip/"
        )

        add_static_image_to_video(image_path, audio_path, clip_path, output_path)

    return render_template("merge.html")  # , message=message)


@app.route("/", methods=["GET", "POST"])
def main():
    global main_topics
    global script_assistant_instance
    global music_gen_instance

    # 사용자 입력을 저장할 변수 초기화
    user_input = ""

    # subtopic-form을 보여줄지 여부를 저장하는 변수
    show_subtopic_form = False

    # 사용자가 선택한 LLM 모델
    selected_model = None

    # POST 요청 처리
    if request.method == "POST":
        print("request:", request)
        print("request.form:", request.form)
        if request.form:
            user_input = request.form.get("user_input")
            selected_model = request.form.get("modelSelect")

            # "주제 생성" 버튼이 눌린 경우
            if "main-button" in request.form:
                # 영상 주제 / 모델이 없다면 입력 혹은 선택하라고 사용자에게 피드백 flash
                if not user_input or not selected_model:
                    flash(
                        "🚨 영상 주제를 입력해주세요❗" if not user_input else "🚨 모델을 선택해주세요❗",
                        "error",
                    )
                else:
                    # ScriptAssistant 인스턴스 생성 또는 업데이트
                    script_assistant_instance = ScriptAssistant(selected_model)

                    # ScriptAssistant 인스턴스가 생성되어 있을 경우에만 make_maintopic 호출 - 주제 생성
                    if script_assistant_instance:
                        main_topics = script_assistant_instance.make_maintopic(
                            user_input
                        )
                        show_subtopic_form = True

                    # musicGen 인스턴스가 생성되어 있는 경우, 병렬로 배경음악 생성 시작
                    # 배경음악 생성에 시간이 걸려서, "주제 생성" 버튼이 눌렸을 때 생성하기 시작함
                    if music_gen_instance:
                        user_input_en = script_assistant_instance.translate2en(
                            user_input
                        )
                        session["user_input_en"] = user_input_en

                        print("===== BGM 생성을 시작합니다. =====")
                        bgm_thread = threading.Thread(
                            target=music_gen_instance.make_bgm, args=(user_input_en,)
                        )
                        bgm_thread.start()

            # "대본 상세 구성하기"이 클릭된 경우
            elif "sub-button" in request.form:
                # 선택한 maintopic
                selected_maintopic = request.form.get("maintopic")

                # 선택된 main topic이 없다면 선택하라고 사용자에게 피드백 flash
                if not selected_maintopic:
                    flash("🚨 메인 주제들 중 하나를 선택해주세요❗", "error")
                    show_subtopic_form = True
                else:
                    if script_assistant_instance:
                        # 소주제 생성하고, subtopic.html 페이지로 리다이렉트
                        subtopics = script_assistant_instance.make_subtopics(
                            user_input, selected_maintopic
                        )

                        # session에 데이터 저장
                        session["user_input"] = user_input
                        session["selected_model"] = selected_model
                        session["selected_maintopic"] = selected_maintopic
                        session["subtopics"] = subtopics

                        # script.html 페이지로 리다이렉트
                        return redirect(url_for("script"))

    return render_template(
        "main.html",
        main_topics=main_topics,
        show_subtopic_form=show_subtopic_form,
        user_input=user_input,
        selected_model=selected_model,
    )


@app.route("/script", methods=["GET", "POST"], endpoint="script")
def script():
    global background_music_option

    # session에 저장된 데이터 불러옴
    user_input = session.get("user_input", "")
    user_input_en = session.get("user_input_en", "")
    selected_model = session.get("selected_model", "")
    selected_maintopic = session.get("selected_maintopic", "")
    subtopics = session.get("subtopics", "")

    # model image 불러오기
    gemini_logo = os.path.join(app.config["IMAGE_FOLDER"], "Gemini.png")
    gpt_logo = os.path.join(app.config["IMAGE_FOLDER"], "GPT.png")

    # POST 요청 처리
    if request.method == "POST":
        print("request:", request)
        print("request.form:", request.form)

        # 배경음악을 선택한 경우
        if "backgroundmusic" in request.json:
            background_music_option = request.json["backgroundmusic"]
            print("BGM 선택!!!", background_music_option)

        # "스크립트 생성" 버튼이 눌린 경우, request.json으로 data가 들어옴(script.js의 fetch 참고)
        elif "script_button" in request.json:
            print("request.json:", request.json)

            # checkedNames : 선택된 체크박스의 name(subtopic{i})들을 리스트로 반환(script.js의 getCheckedCheckboxNames 참고)
            checkedNames = request.json["checkedNames"]

            # ScriptAssistant 인스턴스가 생성되어 있을 경우에만 make_scripts 호출
            if script_assistant_instance:
                # selected_idx : subtopic{i}의 숫자"i"만 추출
                selected_idx = list(map(lambda name: int(name[8:]), checkedNames))
                print("선택된 소주제 번호:", selected_idx)

                # selected_list : selected_idx에 해당하는 영어 subtopic
                selected_list = script_assistant_instance.select_subtopics(selected_idx)

                # 선택된 소주제에 대한 스크립트 생성
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
                            print(f"===== {i+1}번째 스크립트를 작성합니다. =====")
                            for chunk in script_assistant_instance.make_scripts(
                                selected_maintopic, selected_list, str(i + 1)
                            ):
                                print(chunk)
                                if chunk:
                                    yield chunk
                                else:
                                    # Gemini가 empty string을 생성하고 작동을 멈추는 경우가 있기 때문에, 에러를 발생시킴
                                    raise Exception("⚠️ 에러가 발생했습니다! 다시 생성해주세요. ⚠️")
                            print(f"===== {i+1}번째 스크립트를 작성 완료! =====")
                            yield "End of script"
                        yield "The end"
                    except Exception as e:
                        # 디버깅을 위해 exception 로깅
                        print(f"Error: {e}")
                        # client로 에러 메세지 전송
                        yield f"Error: {e}"

                return Response(event_stream(), mimetype="text/event-stream")

        # "영상 만들기" 버튼이 눌린 경우
        elif "video_button" in request.json:
            script_data = request.json.get("scriptData")
            session["script_data"] = script_data

            # video.html 페이지로 리다이렉트 - flask에서 안 되서 js에서 함ㅠ
            # return redirect(url_for("video"))

    print("BGM 기본값:", background_music_option)

    # 템플릿 렌더링. 변수들을 템플릿으로 전달
    return render_template(
        "script.html",
        gemini_logo=gemini_logo,
        gpt_logo=gpt_logo,
        user_input=user_input,
        selected_model=selected_model,
        selected_maintopic=selected_maintopic,
        subtopics=subtopics,
        user_input_en=user_input_en,
    )


@app.route("/video", methods=["GET", "POST"], endpoint="video")
def video():
    print("Reached the /video endpoint.")
    script_data = session.get("script_data", "")
    # ScriptSplitter 인스턴스 생성 또는 업데이트
    script_splitter_instance = ScriptSplitter()
    script_list = script_splitter_instance.split_script2sentences(script_data)
    print(script_list)

    return render_template("video.html", script_list=script_list)


if __name__ == "__main__":
    app.run(debug=True)
