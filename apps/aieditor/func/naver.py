import os
import sys
import urllib.request

# API 인증 정보 설정
client_id = "YOUR_CLIENT_ID"  # 클라이언트 ID
client_secret = "YOUR_CLIENT_SECRET"  # 클라이언트 시크릿

# 변환할 텍스트 인코딩
encText = urllib.parse.quote("지금보다 어리고 민감하던 시절 아버지가 충고를 한마디 했는데 아직도 그 말이 기억난다. 누군가를 비판하고 싶을 때는 이 점을 기억해두는 것이 좋을거다. 세상의 모든 사람이 다 너처럼 유리한 입장에 서 있지는 않다는 것을")

# TTS 요청 파라미터 설정
data = "speaker=nsujin&volume=0&speed=0&pitch=0&format=mp3&text=" + encText;

# TTS 서비스 요청 URL
url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

# 요청 객체 생성 및 헤더 설정
request = urllib.request.Request(url)
request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
request.add_header("X-NCP-APIGW-API-KEY",client_secret)

# TTS 서비스 요청 및 응답 수신
response = urllib.request.urlopen(request, data=data.encode('utf-8'))
rescode = response.getcode()

# 응답 처리
if(rescode==200):
    print("TTS mp3 저장")
    response_body = response.read()
    with open('naver.mp3', 'wb') as f:
        f.write(response_body)  # 응답받은 오디오 데이터를 MP3 파일로 저장
else:
    print("Error Code:" + rescode)  # 오류 발생 시 오류 코드 출력
