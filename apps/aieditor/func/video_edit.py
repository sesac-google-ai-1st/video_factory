from moviepy.editor import *
from moviepy.video.tools.subtitles import *
from moviepy.config import change_settings
from mutagen.mp4 import MP4
import datetime
import os
from moviepy.video.fx.all import *

# change_settings(
#     {"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}
# )

# 데이터 폴더/파일 경로(img, audio, test, video, subtitle)

subtitle_text = ["1_dfssdf", "2_asdf", "3sdfs", "last song!"]


def add_static_image_to_video(image_path, audio_path, output_path):
    """_summary_
    같은 이름의 image와 audio 파일을 합쳐서 video로 만드는 함수
    image path와 audio path, output path를 인수로 주면 이미지 폴더와 오디오폴더 속 파일을 합쳐 output 폴더로 동영상울 출력합니다. 영상간의 transition은 따로 출력되어 output 파일에 저장됩니다.

    이미지와 오디오가 합쳐진 영상과 영상간의 transition이 합쳐져 merge_video로 출력됩니다.
    """
    image_files = os.listdir(image_path)  # image와 audio 파일을 받아 list로 저장
    audio_files = os.listdir(audio_path)

    # empty list 생성
    clips = []
    video_clips = []

    for image_file, audio_file in zip(image_files, audio_files):
        # 오디오 파일 로드
        audio_clip = AudioFileClip(audio_path + audio_file)

        # 이미지 파일을 오디오 길이만큼 보여주는 클립 생성
        image_clip = ImageClip(image_path + image_file, duration=audio_clip.duration)

        # 이미지 클립에 오디오 추가
        video_clip = image_clip.set_audio(audio_clip)

        # 비디오 파일을 만들어 클립 리스트에 추가
        clip_name = os.path.splitext(image_file)[0]
        video_clip.write_videofile(output_path + f"{clip_name}.mp4", fps=24)
        clips.append(video_clip)
    # print(clips)

    # output path 폴더로 이동
    folderName = os.path.split(output_path)[-1]
    os.chdir(f"{folderName}")

    # clip들 간의 transition 생성하기
    for i in range(len(clips)):
        clip = clips[i]
        video_clips.append(clip)

        # vid_transition 파일을 활용하여 video간의 트랜지션 비디오를 출력
        os.system(
            f"python vid_transition.py -i {i+1}.mp4 {i+2}.mp4 --animation translation --num_frames 30 --max_brightness 1.5"
        )

        # 트랜지션 비디오가 있으면 video_vlips에 추가, 없으면 패스
        if os.path.exists(output_path + f"vt{i+1}_phase1.mp4") == True:
            trans_clips1 = VideoFileClip(output_path + f"vt{i+1}_phase1.mp4")
            video_clips.append(trans_clips1)
            trans_clips2 = VideoFileClip(output_path + f"vt{i+1}_phase2.mp4")
            video_clips.append(trans_clips2)

    # 모든 클립을 하나로 합치기
    final_clip = concatenate_videoclips(video_clips, method="compose")

    # 결과 영상 파일 생성
    final_clip.write_videofile(output_path + "merge_video.mp4", fps=24)


# 자막 파일 생성하기
def make_subtitle(audio_path, video_path, txt_list):
    """_summary_
    audio 파일과 video 파일을 대조하여 video 길이를 측정,
    자막을 list 형태로 전달하면 트랜지션 시간을 제외한 video가 나오는 부분에만 자막을 생성할 수 있도록 합니다.

    자막 파일은 sample.srt 파일로 작성됩니다.

    Args:
        audio_path (str): audio 파일이 들어있는 폴더를 지정합니다.
        video_path (str): video 파일이 들어있는 폴더를 지정합니다.
        txt_list (list): 자막에 들어갈 텍스트를 리스트 형태로 받습니다.
    """
    srt = open("sample.srt", "w+")

    # empty list 생성
    second_list = []
    hhms = []

    # 첫번째 파일은 앞에 transition이 없기 때문에 따로 리스트에 추가합니다.
    filename = video_path + "1.mp4"
    video = VideoFileClip(filename)
    length = video.duration
    second_list.append(length)

    # 비디오 간 transition이 2.5초이기 때문에 자막 텍스트 간에 공백을 둡니다.
    for i in range(len(os.listdir(audio_path)) - 1):
        second_list.append(2.5)
        filename = video_path + f"{i+2}.mp4"
        video = VideoFileClip(filename)
        length = video.duration
        second_list.append(length)
    second = second_list

    # second_list에 기록되어있는 초들끼리 더하여 타임라인 리스트를 만듭니다.
    for i in range(len(second_list)):
        if i == 0:
            second[0] = second_list[0]
        else:
            second[i] = float(second_list[i - 1]) + float(second_list[i])

    # 00초를 먼저 추가한 후 타임라인 리스트를 time 형식으로 처리합니다.
    hhms.append(str("0:00:00,000"))
    for f in second_list:
        time = str(datetime.timedelta(seconds=f)).replace(".", ",")
        hhms.append(time)
    print(hhms)

    # 처리한 리스트로 srt 파일을 작성합니다.
    for i in range(len(hhms) // 2):
        srt.write(f"%d\n{hhms[2*i]} --> {hhms[2*i+1]}\n{txt_list[i]}\n\n" % (i + 1))


def subtitles(video_file, subtitle_file, output_path):
    """_summary_
    앞서 만들어진 subtitle 자막을 video에 나타내는 코드입니다.

    Args:
        video_file (str): video file의 절대 경로를 입력합니다.
        subtitle_file (_type_): subtitle 파일의 경로를 입력합니다. (여기서는 sample.srt)
        output_path (_type_): 자막이 생성된 비디오가 저장될 경로를 지정합니다.
    """

    # 자막 서식을 작성합니다.
    generator = lambda txt: TextClip(
        txt, font="Georgia-Regular", fontsize=50, color="white", bg_color="grey"
    )
    video_clip = VideoFileClip(video_file)
    subtitles_clip = SubtitlesClip(subtitle_file, generator)

    # 앞서 작성한 subtitles_clip이 video_clip의 길이동안 지속되도록 세팅합니다.
    subtitles_clip = subtitles_clip.set_position(("center", "bottom")).set_duration(
        video_clip.duration
    )

    # video_clip과 subtitle_clip을 combine합니다.
    final_clip = CompositeVideoClip(
        [video_clip, subtitles_clip.set_pos(("center", "bottom"))]
    )

    # 최종적으로 합쳐진 비디오를 subtitle_video라는 이름으로 출력합니다.
    final_clip.write_videofile(output_path + "subtitle_video.mp4")


# add_static_image_to_video(img, audio, test)
# make_subtitle(audio, test, subtitle_text)
# subtitles(video, subtitle, test)
