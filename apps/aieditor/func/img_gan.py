from openai import OpenAI
import requests

# diffusers 모델 돌릴때
from diffusers import AutoPipelineForText2Image
from PIL import Image, ImageDraw, ImageFont
import platform
import textwrap


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def pil_draw_label(
    image,
    text,
    font_color=(255, 255, 255),
    font_size=18,
    max_line_length=32,
    bottom_margin=20,
):
    width, height = image.size
    draw = ImageDraw.Draw(image)
    if platform.system() == "Darwin":  # 맥
        font = "AppleGothic.ttf"
    elif platform.system() == "Windows":  # 윈도우
        font = "malgunbd.ttf"
    elif platform.system() == "Linux":  # 리눅스 (구글 콜랩)
        """
        !wget "https://www.wfonts.com/download/data/2016/06/13/malgun-gothic/malgunbd.ttf"
        !mv malgun.ttf /usr/share/fonts/truetype/
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
    for line in wrapped_text.split("\n"):
        line_width, line_height = textsize(line, font=imageFont)
        total_text_height += line_height

    # Calculate the starting position to center the wrapped text at the bottom
    x = (width - max_line_length) // 2  # Adjust if needed
    y = height - total_text_height - bottom_margin  # Added margin

    # Draw each line of the wrapped text
    for line in wrapped_text.split("\n"):
        line_width, line_height = textsize(line, font=imageFont)
        draw.text(((width - line_width) // 2, y), line, font=imageFont, fill=font_color)
        y += line_height

    return image


def img_gan_prompt(maintheme, scripts):
    """
    이미지 생성을 위한 프롬프트 생성 함수
    인수 메인테마, 스크립트 : list 변수
    """
    prompts = []
    for prompt in scripts:
        prompts.append(
            f"영상의 주제에 맞춰서 이미지(장면)를 그려줘, 영상 주제는 {maintheme}이고, 제작 요청 이미지 : {prompt}. 주의!!! 영상 주제({maintheme})에 어울리게 이미지를 그려줘"
        )
    return prompts


# img_gan_prompt(maintheme, scripts)
# print(prompts)


def img_gan_dalle3(api_key, prompts, progress_callback=None):
    """
    dalle3 모델로 이미지를 생성하는 함수,
    인수 openAI api kes, img_gan_prompt 함수로 생성한 prompts : list
    실행되는 곳에 ./images 폴더가 있어야함, 파일명은 1번 부터 list의 길이 만큼
    """
    client = OpenAI(api_key=api_key)
    # size = "256x256" # dalle2
    # size = "512x512" # dalle2
    size = "1024x1024"  # dalle3
    # size = "1792x1024" # dalle3
    # size = "1024x1792" # dalle3
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

        # 응답 상태 코드가 200 OK 인지 확인합니다.
        img_filename = f"C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/images/{idx+1:0>3}.jpg"

        # 바이너리 쓰기 모드(b)로 파일을 열고 이미지 데이터를 기록합니다.
        with open(img_filename, "wb") as out_file:
            # 이미지 데이터를 파일에 씁니다.
            out_file.write(response.content)
            print(f"이미지 파일이 '{img_filename}'로 저장되었습니다.")

        # Emit progress update to the client
        if progress_callback:
            progress_callback("이미지 생성 중", round(((idx + 1) / len(prompts)) * 100))

    # Generation is complete
    if progress_callback:
        progress_callback("이미지 생성 완료", 100)


# sdxl turbo로 이미지 생성하는 함수
def img_gen_sdxlturb(script, prompts, progress_callback=None, with_sub=False):
    # 파이프 라인 만들기(sdxl turbo 모델 가져오기)
    pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo")

    width = 1280 // 2
    height = 720 // 2

    # Generation start
    if progress_callback:
        progress_callback("이미지 생성 중", 0)

    # 이미지 생성(프롬프트 입력, 추론 스텝 1, 프롬프트 충실도 0)
    for idx, prompt in enumerate(prompts):
        image = pipe(
            prompt=prompt,
            num_inference_steps=1,
            guidance_scale=0.0,
            width=width,
            height=height,
        ).images[0]

        # 이미지 저장
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)

        file_path = f"C:/Users/SBA/Documents/GitHub/video_factory/apps/aieditor/func/images/{idx+1:0>3}.jpg"

        if not with_sub:  # 자막 없는 이미지
            # 이미지 저장
            image.save(file_path)
            print(f"이미지가 {file_path}에 저장되었습니다.")

            # Emit progress update to the client
            if progress_callback:
                progress_callback(
                    "이미지 생성 중",
                    round(((idx + 1) / len(prompts)) * 100),
                    f"/func_images/{idx+1:0>3}.jpg",
                )

        elif with_sub:  # 자막 있는 이미지
            print("자막 있음")
            # Emit progress update to the client
            if progress_callback:
                print("이미지에 자막 다는 중")
                sub = script[idx]
                print(sub)
                # 자막 추가
                image = pil_draw_label(image, sub)

                # 결과 이미지 저장
                image.save(file_path)
                print(f"이미지가 {file_path}에 저장되었습니다.")

                progress_callback(
                    "자막이 합성된 이미지 생성 중",
                    round(((idx + 1) / len(prompts)) * 100),
                    f"/func_images/{idx+1:0>3}.jpg",
                )

    # Generation is complete
    if progress_callback:
        progress_callback("이미지 생성 완료", 100)
