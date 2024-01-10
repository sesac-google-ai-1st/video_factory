from moviepy.editor import *
import os


# image 파일과 mp3 파일을 합치는 함수
def add_static_image_to_audio(image_path, audio_path, output_path):
    audio_files = os.listdir(audio_path)
    file_names = [os.path.splitext(file)[0] for file in audio_files]

    for i in file_names:
        if os.path.isfile(image_path + i + ".jpg"):
            image_clip = ImageClip(image_path + i + ".jpg")
            audio_clip = AudioFileClip(audio_path + i + ".mp3")

            video_clip = image_clip.set_audio(audio_clip)
            video_clip.duration = audio_clip.duration
            video_clip.fps = 1

            video_clip.write_videofile(output_path + i + ".mp4")


# 문장별로 나눠진 mp4 파일을 merge하는 함수
def merge_video(video_path, output_path):
    video_files = os.listdir(video_path)
    video_list = []

    for f in video_files:
        video_clip = VideoFileClip(video_path + f)
        video_list.append(video_clip)

    final_video = concatenate_videoclips(video_list, method="compose")
    print(video_list)

    final_video.write_videofile(output_path + "merged_video.mp4")


# def subtitles(video_path, subtitle_file):

# 데이터 폴더 경로
# img = "C:/Users/SBA/Documents/mainProject/moviepy/image/"
# audio = "C:/Users/SBA/Documents/mainProject/moviepy/audio/"
# test = "C:/Users/SBA/Documents/mainProject/moviepy/test/"
# final = "C:/Users/SBA/Documents/mainProject/moviepy/merge_video/"


# add_static_image_to_audio(img, audio, test)

# merge_video(test, final)
