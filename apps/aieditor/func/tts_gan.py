from google.cloud import texttospeech

# sentences = ["베수비오 화산이 폭발하던 그 순간, 폼페이는 어땠을까요?", "오늘 우리는 그 끔찍한 순간을 들여다봅니다.", "화산재와 용암으로 하늘이 뒤덮였고, 폼페이 사람들은 어떻게 반응했을까요?", "자, 이제 그들의 용기와 우리에게 전하는 메시지", "자연재해 앞에서 우리의 대처 방법을 함께 탐색해봅시다."]  # 실제 문장으로 대체해야 합니다.


def voice_gan_wavenet(sentences, progress_callback=None):
    # 클라이언트 초기화
    client = texttospeech.TextToSpeechClient()

    # 음성 설정
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # 오디오 출력 형식 설정
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # 100개의 서로 다른 문장
    # sentences = ["베수비오 화산이 폭발하던 그 순간, 폼페이는 어땠을까요?", "오늘 우리는 그 끔찍한 순간을 들여다봅니다.", "화산재와 용암으로 하늘이 뒤덮였고, 폼페이 사람들은 어떻게 반응했을까요?", "자, 이제 그들의 용기와 우리에게 전하는 메시지", "자연재해 앞에서 우리의 대처 방법을 함께 탐색해봅시다."]  # 실제 문장으로 대체해야 합니다.

    # 파일 저장을 위한 반복문
    for i, sentence in enumerate(sentences, start=1):
        # 합성할 텍스트 설정
        synthesis_input = texttospeech.SynthesisInput(text=sentence)

        # 텍스트-음성 변환 요청
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # 음성 데이터 저장 (파일명을 i.mp3로 설정)
        filename = f"C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/voice/{i:0>3}.mp3"
        with open(filename, "wb") as out:
            out.write(response.audio_content)
            print(f"오디오 파일이 '{filename}'에 저장되었습니다.")

        # Update progress after each sentence
        if progress_callback:
            progress_callback(round((i / len(sentences)) * 100))

    # Reset progress to 0 after voice generation is complete
    if progress_callback:
        progress_callback(0)
