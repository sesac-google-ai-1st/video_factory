from moviepy.editor import *
from moviepy.video.tools.subtitles import *
from moviepy.config import change_settings
from mutagen.mp3 import MP3
import datetime
import os

# change_settings(
#     {"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}
# )

# 데이터 폴더 경로


def add_static_image_to_video(image_path, audio_path, output_path):
    image_files = os.listdir(image_path)
    audio_files = os.listdir(audio_path)
    clips = []

    for image_file, audio_file in zip(image_files, audio_files):
        # 오디오 파일 로드
        audio_clip = AudioFileClip(audio_path + audio_file)

        # 이미지 파일을 오디오 길이만큼 보여주는 클립 생성
        image_clip = ImageClip(image_path + image_file, duration=audio_clip.duration)

        # 이미지 클립에 오디오 추가
        video_clip = image_clip.set_audio(audio_clip)

        # 클립 리스트에 추가
        clips.append(video_clip)

    # 모든 클립을 하나로 합치기
    final_clip = concatenate_videoclips(clips, method="compose")

    # 결과 영상 파일 생성
    final_clip.write_videofile(output_path + "output_video.mp4", fps=24)


subtitle_text = ["1_dfssdf", "2_asdf", "3sdfs", "last song!"]


# 자막 파일 생성하기
def make_subtitle(audio_path, txt_list):
    audio_list = os.listdir(audio_path)
    srt = open("sample.srt", "w+")
    second_list = []
    hhms = []

    for f in audio_list:
        filename = audio_path + f
        length = float(MP3(filename).info.length)
        second_list.append(length)

    second = second_list
    for i in range(len(second_list)):
        if i == 0:
            second[0] = second_list[0]
        else:
            second[i] = float(second_list[i - 1]) + float(second_list[i])

    hhms.append(str("0:00:00,000"))
    for f in second_list:
        time = str(datetime.timedelta(seconds=f)).replace(".", ",")
        hhms.append(time)
    print(hhms)

    for i in range(len(hhms) - 1):
        srt.write(f"%d\n{hhms[i]} --> {hhms[i+1]}\n{txt_list[i]}\n\n" % (i + 1))
    srt.write(f"%d\n{hhms[-1]} --> {hhms[-1]}\nend\n" % (len(hhms)))


make_subtitle(audio, subtitle_text)


def subtitles(video_file, subtitle_file, output_path):
    generator = lambda txt: TextClip(
        txt, font="Georgia-Regular", fontsize=50, color="white"
    )
    video_clip = VideoFileClip(video_file)

    subtitles_clip = SubtitlesClip(subtitle_file, generator)

    subtitles_clip = subtitles_clip.set_position(("center", "bottom")).set_duration(
        video_clip.duration
    )

    final_clip = CompositeVideoClip(
        [video_clip, subtitles_clip.set_pos(("center", (0.885 * 1220)))]
    )

    final_clip.write_videofile(output_path + "subtitle_video.mp4")


add_static_image_to_video(img, audio, test)
subtitles(video, subtitle, test)
