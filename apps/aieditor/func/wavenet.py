from google.cloud import texttospeech

# 클라이언트 초기화
client = texttospeech.TextToSpeechClient()

# 합성할 텍스트 설정
synthesis_input = texttospeech.SynthesisInput(text="지금보다 어리고 민감하던 시절 아버지가 충고를 한마디 했는데 아직도 그 말이 기억난다. 누군가를 비판하고 싶을 때는 이 점을 기억해두는 것이 좋을거다. 세상의 모든 사람이 다 너처럼 유리한 입장에 서 있지는 않다는 것을")

# 음성 설정: 여기서는 WaveNet 모델을 선택
voice = texttospeech.VoiceSelectionParams(
    language_code="ko-KR",  # 언어 설정 (예: 한국어)
    name="ko-KR-Wavenet-A",  # WaveNet 음성 이름 A, B 여성 C, D 남성
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

# 오디오 출력 형식 설정
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3)

# 텍스트-음성 변환 요청
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config)

# 음성 데이터 저장
with open("wavenetA.mp3", "wb") as out:
    out.write(response.audio_content)
    print("오디오 파일이 'wavenetA.mp3'에 저장되었습니다.") 
