from img_gan import img_gan_prompt, img_gan_dalle3
import time

api_key = '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'

start_time = time.time()

maintheme = "폼페이의 마지막 날"
scripts = ["베수비오 화산이 폭발하던 그 순간, 폼페이는 어땠을까요?",
           "오늘 우리는 그 끔찍한 순간을 들여다봅니다.",
           "화산재와 용암으로 하늘이 뒤덮였고, 폼페이 사람들은 어떻게 반응했을까요?",
           "자, 이제 그들의 용기와 우리에게 전하는 메시지, 자연재해 앞에서 우리의 대처 방법을 함께 탐색해봅시다."
          ]

# 프롬프트 리스트 생성 img_gan_prompt(영상메인 테마, 스크립트 리스트)
prompts = img_gan_prompt(maintheme, scripts)

# 이미지 생성 img_gan_dall3(api_key, 위에서 생성된 프롬프트 )
img_gan_dalle3(api_key, prompts)


