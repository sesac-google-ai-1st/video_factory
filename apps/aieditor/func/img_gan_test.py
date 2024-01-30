import time
from flask import Flask, render_template
import os
from split_script import ScriptSplitter
from tts_gan import voice_gan_wavenet
from img_gan import img_gan_prompt, img_gan_dalle3
from video_edit import add_static_image_to_video, make_subtitle


api_key = ''

# start_time = time.time()

maintheme = "폼페이의 마지막 날"


scripts = ["베수비오 화산이 폭발하던 그 순간, 폼페이는 어땠을까요? \
            오늘 우리는 그 끔찍한 순간을 들여다봅니다. \
            화산재와 용암으로 하늘이 뒤덮였고, 폼페이 사람들은 어떻게 반응했을까요? \
            자, 이제 그들의 용기와 우리에게 전하는 메시지, 자연재해 앞에서 우리의 대처 방법을 함께 탐색해봅시다."
           ]

# @app.route("/merge", methods=["GET", "POST"], endpoint="merge")
# def merge():
# 1) 스크립트를 문장 단위로 나누줌, list로 출력
# from split_script import ScriptSplitter

# splits = ScriptSplitter()
# split_text = splits.split_script2sentences(scripts)
# print(split_text)


# # 2) 더빙 음성 생성
# from tts_gan import voice_gan_wavenet
# # voice_gan_wavenet(split_text)


# 3) 이미지 생성
# 이미지 생성을 위한 프롬프트 리스트 생성 : img_gan_prompt(영상메인 테마, 스크립트 리스트)
# from img_gan import img_gan_prompt, img_gan_dalle3

# prompts = img_gan_prompt(maintheme, split_text)

# 이미지 생성 img_gan_dall3(api_key, 위에서 생성된 프롬프트), images 폴더에 저장됨
# img_gan_dalle3(api_key, prompts)


# # 4)영상 합치기
from video_edit import add_static_image_to_video

# # 이미지를 더빙 음성 길이 맞춰 비디오 클립 생성 + 비디오 클립 음성 더빙 병합
# image_path = "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/images/"
# audio_path = "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/voice/"
# clip_path = "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/clip/"

image_path = "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/images/"
audio_path = "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/voice/"
clip_path = "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/clip/"
output_path = "C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/finalclip/"

add_static_image_to_video(image_path, audio_path, clip_path, output_path)

# def add_static_image_to_video(image_path, audio_path, clip_path, output_path):
# # 5) 자막파일 만들기
# from video_edit import make_subtitle

# # def make_subtitle(audio_path, video_path, txt_list):
# make_subtitle(audio_path, clip_path, split_text)
