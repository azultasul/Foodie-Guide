import openai
import requests
import os

import dotenv
dotenv.load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 최신 SDK 방식으로 클라이언트 생성
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_and_download_image(prompt: str, save_path: str = "cache/generated_image.png", size: str = "256x256"):
    try:
        # 이미지 생성 요청
        response = client.images.generate(
            model="dall-e-3",  # 또는 "dall-e-2" (속도 vs. 품질 선택 가능)
            prompt=prompt,
            size=size,
            quality="standard",  # "hd" 옵션은 dall-e-3에서만 사용 가능
            n=1
        )

        # 이미지 URL 가져오기
        image_url = response.data[0].url
        print(f"Image URL: {image_url}")

        # 이미지 다운로드
        img_data = requests.get(image_url).content
        with open(save_path, 'wb') as handler:
            handler.write(img_data)

        print(f"✅ Image saved to {save_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

# 예시 사용
generate_and_download_image(
    prompt="김치찌개",
    save_path="./cache/김치찌개.png",
    size="1024x1024"
)
