from openai import OpenAI
import requests

# diffusers 모델 돌릴때
from diffusers import AutoPipelineForText2Image
from PIL import Image, ImageDraw, ImageFont

import platform
import textwrap
from io import BytesIO
import os
import torch


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def pil_draw_label(
    image,
    text,
    font_color=(255, 255, 255),
    font_size=32,
    max_line_length=65,
    bottom_margin=50,
):
    """이미지에 자막을 넣는 함수입니다.

    Args:
        image (Image): 이미지 객체
        text (str): 이미지에 들어갈 자막 문자열
        font_color (tuple, optional): 자막의 글씨 색깔. Defaults to (255, 255, 255).
        font_size (int, optional): 자막의 글씨 크기. Defaults to 32.
        max_line_length (int, optional): 자막의 최대 가로 길이. 자막의 가로 길이가 이미지의 가로 길이보다 크면 자막이 잘림. Defaults to 65.
        bottom_margin (int, optional): 자막의 위치. 이미지 하단에서 얼마나 떨어져있는지를 정하는 변수. Defaults to 50.

    Returns:
        Image: 자막이 합성된 이미지
    """
    width, height = image.size
    draw = ImageDraw.Draw(image, "RGBA")
    if platform.system() == "Darwin":  # 맥
        font = "AppleGothic.ttf"
    elif platform.system() == "Windows":  # 윈도우
        font = "malgunbd.ttf"
    elif platform.system() == "Linux":  # 리눅스
        """
        !wget "https://www.wfonts.com/download/data/2016/06/13/malgun-gothic/malgunbd.ttf"
        !mv malgundb.ttf /usr/share/fonts/truetype/
        import matplotlib.font_manager as fm
        fm._rebuild()
        """
        font = "malgunbd.ttf"
    try:
        imageFont = ImageFont.truetype(font, font_size)
    except:
        imageFont = ImageFont.load_default()

    # Wrap the text based on max_line_length
    wrapped_text = textwrap.fill(text, width=max_line_length)

    # Calculate the total height of the wrapped text
    total_text_height = 0
    lines = wrapped_text.split("\n")
    for line in lines:
        line_width, line_height = textsize(line, font=imageFont)
        total_text_height += line_height

    # Calculate the starting position to center the wrapped text at the bottom
    y = height - total_text_height - bottom_margin  # Added margin
    add_padding = 5

    # Draw each line of the wrapped text with background rectangle
    for line in lines:
        line_width, line_height = textsize(line, font=imageFont)
        x = (width - line_width) // 2
        bg_color = (0, 0, 0, 128)  # Black with 50% opacity
        bg_height = line_height + add_padding  # Added padding
        draw.rectangle(
            [(x - add_padding, y), (x + line_width + add_padding, y + bg_height)],
            fill=bg_color,
        )
        draw.text((x, y), line, font=imageFont, fill=font_color)
        y += bg_height + 1

    return image


def img_gan_prompt(lang, maintheme, scripts):
    """
    이미지 생성을 위한 프롬프트 생성 함수
    인수 메인테마, 스크립트 : list 변수
    """
    prompts = []

    if lang == "ko":
        for prompt in scripts:
            prompts.append(
                f"영상 주제에 맞춰서 이미지(장면)를 그려줘, 영상 주제는 '{maintheme}'이고, 제작 요청 이미지 : {prompt}. 주의!!! 영상 주제({maintheme})에 어울리게 이미지를 그려줘"
            )
        return prompts
    else:
        for prompt in scripts:
            prompts.append(
                f"""Draw an image (scene) that matches the theme of the video. Video theme: "{maintheme}"
                Requested image: {prompt}"""
            )
        return prompts


# img_gan_prompt(maintheme, scripts)
# print(prompts)


def img_gan_dalle3(
    api_key, script, prompts, output_folder, progress_callback=None, with_sub=False
):
    """
    dalle3 모델로 이미지를 생성하는 함수,
    인수 openAI api kes, img_gan_prompt 함수로 생성한 prompts : list
    실행되는 곳에 ./images 폴더가 있어야함, 파일명은 1번 부터 list의 길이 만큼
    """
    client = OpenAI(api_key=api_key)
    # size = "256x256" # dalle2
    # size = "512x512" # dalle2
    # size = "1024x1024"  # dalle3
    size = "1792x1024"  # dalle3
    # size = "1024x1792" # dalle3

    # 응답 상태 코드가 200 OK 인지 확인합니다.
    output_folder = output_folder
    # output_folder가 없으면 만듦
    os.makedirs(output_folder, exist_ok=True)

    # Generation start
    if progress_callback:
        progress_callback("이미지 생성 중", 0, step_now=2)

    for idx, prompt in enumerate(prompts):
        response = client.images.generate(
            model="dall-e-3",  # 모델명
            prompt=prompt,  # 생성할 이미지에 대한 설명
            size=size,  # 이미지의 크기
            quality="standard",  # 이미지의 품질
            n=1,  # 생성할 이미지의 개수
        )

        # 생성된 이미지의 URL 추출
        image_url = response.data[0].url

        # stream=True 옵션을 사용하여 서버로부터 데이터를 바로 파일로 저장할 수 있도록 합니다.
        response = requests.get(image_url, stream=True)

        output_path = os.path.join(output_folder, f"{idx+1:0>3}.jpg")

        if not with_sub:  # 자막 없는 이미지
            # 바이너리 쓰기 모드(b)로 파일을 열고 이미지 데이터를 기록합니다.
            with open(output_path, "wb") as out_file:
                # 이미지 데이터를 파일에 씁니다.
                out_file.write(response.content)
                print(f"이미지 파일이 '{output_path}'로 저장되었습니다.")

            # Emit progress update to the client
            if progress_callback:
                progress_callback(
                    "이미지 생성 중",
                    round(((idx + 1) / len(prompts)) * 100),
                    image_url=f"/show_images/{idx+1:0>3}.jpg",
                    step_now=2,
                )

        elif with_sub:  # 자막 있는 이미지
            print("자막 있음")
            # Emit progress update to the client
            if progress_callback:
                sub = script[idx]
                print("자막", sub)
                # 자막 추가
                image = pil_draw_label(Image.open(BytesIO(response.content)), sub)  ####

                # 결과 이미지 저장
                image.save(output_path)
                print(f"이미지가 {output_path}에 저장되었습니다.")

                progress_callback(
                    "자막이 합성된 이미지 생성 중",
                    round(((idx + 1) / len(prompts)) * 100),
                    image_url=f"/show_images/{idx+1:0>3}.jpg",
                    step_now=2,
                )

    # Generation is complete
    if progress_callback:
        progress_callback("이미지 생성 완료", 100, step_now=2)


# sdxl turbo로 이미지 생성하는 함수
def img_gen_sdxlturb(
    script, prompts, output_folder, progress_callback=None, with_sub=False
):
    """
    stable diffusion sdxlturb 모델로 이미지를 생성하는 함수,
    인수 img_gan_prompt 함수로 생성한 prompts : list
    실행되는 곳에 ./images 폴더가 있어야함, 파일명은 1번 부터 list의 길이 만큼
    """
    # cuda gpu사용 가능한지 여부 확인
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Stable diffusion using device : {device}")

    # 파이프 라인 만들기(sdxl turbo 모델 가져오기)
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
        )
        pipe.to("cuda")
    else:
        pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo")

    width = 1280
    height = 720

    output_folder = output_folder
    # output_folder가 없으면 만듦
    os.makedirs(output_folder, exist_ok=True)

    # Generation start
    if progress_callback:
        progress_callback("이미지 생성 중", 0, step_now=2)

    # 이미지 생성(프롬프트 입력, 추론 스텝 1, 프롬프트 충실도 0)
    for idx, prompt in enumerate(prompts):
        image = pipe(
            prompt=prompt,
            num_inference_steps=4,
            guidance_scale=0.0,
            width=width,
            height=height,
        ).images[0]

        # 이미지 저장
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)

        output_path = os.path.join(output_folder, f"{idx+1:0>3}.jpg")

        if not with_sub:  # 자막 없는 이미지
            # 이미지 저장
            image.save(output_path)
            print(f"이미지가 {output_path}에 저장되었습니다.")

            # Emit progress update to the client
            if progress_callback:
                progress_callback(
                    "이미지 생성 중",
                    round(((idx + 1) / len(prompts)) * 100),
                    image_url=f"/show_images/{idx+1:0>3}.jpg",
                    step_now=2,
                )

        elif with_sub:  # 자막 있는 이미지
            print("자막 있음")
            # Emit progress update to the client
            if progress_callback:
                sub = script[idx]
                print("자막 :", sub)
                # 자막 추가
                image = pil_draw_label(
                    image,
                    sub,
                    font_size=25,
                    max_line_length=50,
                    bottom_margin=40,
                )

                # 결과 이미지 저장
                image.save(output_path)
                print(f"이미지가 {output_path}에 저장되었습니다.")

                progress_callback(
                    "자막이 합성된 이미지 생성 중",
                    round(((idx + 1) / len(prompts)) * 100),
                    image_url=f"/show_images/{idx+1:0>3}.jpg",
                    step_now=2,
                )

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # Generation is complete
    if progress_callback:
        progress_callback("이미지 생성 완료", 100, step_now=2)
