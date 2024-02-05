from openai import OpenAI
import requests

# diffusers 모델 돌릴때
from diffusers import AutoPipelineForText2Image
from PIL import Image


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
def img_gen_sdxlturb(prompts, progress_callback=None):
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

    # Generation is complete
    if progress_callback:
        progress_callback("이미지 생성 완료", 100)
