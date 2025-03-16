from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import requests


load_dotenv() 

app = Flask(__name__)
CORS(app)  # Vite 프론트엔드와 CORS 문제 방지

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY) 

# Naver
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# NCP
NCP_CLIENT_ID = os.getenv("NCP_CLIENT_ID")
NCP_CLIENT_SECRET = os.getenv("NCP_CLIENT_SECRET")

@app.route("/")
def home():

    # 검색어 및 요청 URL 설정
    query = "강남역 카페"  # 검색어 (예: "카페", "맛집", "미용실" 등)
    display = 5  # 출력할 검색 결과 개수 (최대 5)
    start = 1  # 검색 시작 위치 (1부터 시작)
    sort = "random"  # 정렬 방식 (sim: 유사도순, random: 랜덤)

    url = f"https://openapi.naver.com/v1/search/local.json?query={query}&display={display}&start={start}&sort={sort}&mapx=100"

    # HTTP 요청 헤더 설정
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    # API 요청 (GET)
    response = requests.get(url, headers=headers)

    
    
    # 응답 확인
    if response.status_code == 200:
        items = []
        data = response.json()
        for item in data["items"]:
            one = {}
            one["title"] = item["title"]
            one["lat"] = float(item["mapy"])/1e7
            one["lng"] = float(item["mapx"])/1e7
            one["link"] = item["link"]
            items.append(one)
            # print(f"이름: {item["title"]}, 위치: {float(item["mapx"])/1e7}, {float(item["mapy"])/1e7}")
            # print(f"이름: {item['title']}\n주소: {item['address']}\n전화번호: {item['telephone']}\n링크: {item['link']}\n")
        return render_template("index.html", NCP_CLIENT_ID=NCP_CLIENT_ID, items=items)
    else:
        print("Error Code:", response.status_code)
        print("Error Message:", response.content)
        return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = f"오류 발생: {str(e)}"

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
