import os
import sys
import urllib.request

# API 인증 정보 설정
client_id = "YOUR_CLIENT_ID"  # 클라이언트 ID
client_secret = "YOUR_CLIENT_SECRET"  # 클라이언트 시크릿


def voice_gan_naver(sentences, output_folder, progress_callback=None):
    output_folder = output_folder
    # output_folder가 없으면 만듦
    os.makedirs(output_folder, exist_ok=True)

    # Generation start
    if progress_callback:
        progress_callback("나레이션 생성 중", 0, step_now=1)

    # 파일 저장을 위한 반복문
    for i, sentence in enumerate(sentences, start=1):
        # 변환할 텍스트 인코딩
        encText = urllib.parse.quote(sentence)

        # TTS 요청 파라미터 설정
        data = "speaker=napple&volume=0&speed=-1&pitch=0&format=mp3&text=" + encText

        # TTS 서비스 요청 URL
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

        # 요청 객체 생성 및 헤더 설정
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)

        # TTS 서비스 요청 및 응답 수신
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()

        # 응답 처리
        if rescode == 200:
            # 음성 데이터 저장 (파일명을 00i.mp3로 설정)
            output_path = os.path.join(output_folder, f"{i:0>3}.mp3")

            response_body = response.read()
            with open(output_path, "wb") as f:
                f.write(response_body)  # 응답받은 오디오 데이터를 MP3 파일로 저장
                print(f"naver 오디오 파일이 '{output_path}'에 저장되었습니다.")
            # Update progress after each sentence
            if progress_callback:
                progress_callback(
                    "나레이션 생성 중", round((i / len(sentences)) * 100), step_now=1
                )

        else:
            print("Error Code:" + rescode)  # 오류 발생 시 오류 코드 출력

    # Generation is complete
    if progress_callback:
        progress_callback("나레이션 생성 완료", 100, step_now=1)
