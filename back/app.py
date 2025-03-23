from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS
import openai
import os
import numpy as np
from math import radians, sin, cos, sqrt, atan2
from dotenv import load_dotenv
import requests
from RAG import RAG

load_dotenv() 

app = Flask(__name__)
app.secret_key = "1234"
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
def sitemap():
    return render_template('sitemap.html')

@app.route("/home")
def home():
    if not session.get('address'):  # 주소 정보가 없으면 초기화
        session['address'] = None
    global messages
    messages = []
    messages.append({"role": "system", "content": "너는 음식 메뉴를 추천하는 AI야."})
    return render_template("index.html", address = session['address'])

@app.route("/navermap", methods=["POST"])
def navermap():
    
    latitude = request.form.get("latitude", None)  # 위도
    longitude = request.form.get("longitude", None)  # 경도
    session['address'] = request.form.get("address", None)  # 주소
    menus_str = request.form.get("menus", None)  # 검색어 (예: "카페", "맛집", "미용실" 등)

    print("/navermap:", latitude, longitude, session['address'], menus_str)
    
    items = search_store(session['address'], menus_str)
    nearest_idx = calculate_nearest_store_index(items, float(latitude), float(longitude))
    return render_template("navermap.html", latitude=latitude, longitude=longitude, address=session['address'],
                           NCP_CLIENT_ID=NCP_CLIENT_ID, query=menus_str, items=items, nearest_idx=nearest_idx)

def search_store(address, menus_str):
    if menus_str == None or menus_str == "":
        menus_str = "맛집"
    menus = menus_str.split(",")
    
    items = []
    for menu in menus:
        query = address + " " + menu
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
            data = response.json()
            for item in data["items"]:
                one = {}
                one["title"] = item["title"].replace("<b>", "").replace("</b>", "").replace("&amp;", "&")
                one["lat"] = float(item["mapy"])/1e7
                one["lng"] = float(item["mapx"])/1e7
                one["link"] = item["link"]
                dist = haversine(one["lat"], one["lng"], session['latitude'], session['longitude'])
                one["dist"] = "{:.1f}".format(dist)
                one["category"] = item["category"]
                one["address"] = item["address"]
                items.append(one)
                
        else:
            print("Error Code:", response.status_code)
            print("Error Message:", response.content)
            # return render_template("navermap.html")
    return items

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (단위: km)

    # 위도와 경도를 라디안 단위로 변환
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # 위도/경도의 차이 계산
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine 공식
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def calculate_nearest_store_index(items, latitude, longitude):
    min_distance = 1e9
    nearest_index = -1
    for i, item in enumerate(items):
        distance = (item["lat"] - latitude)**2 + (item["lng"] - longitude)**2
        if distance < min_distance:
            min_distance = distance
            nearest_index = i
    return nearest_index

@app.route("/navergeocode", methods=["POST", "GET"])
def navergeocode():
    if request.method == "GET":
        latitude = 37.5665   # 위도 (서울)
        longitude = 126.978  # 경도 (서울)
        address = reverse_geocode(latitude, longitude)[2]
    else:
        latitude = request.json["latitude"]
        longitude = request.json["longitude"]
        print('/navergeocode:',latitude, longitude)
        if latitude == None or longitude == None:
            address = ""
        else:
            address = reverse_geocode(latitude, longitude)[2]
        
    items = {}
    items['latitude'] = latitude
    items['longitude'] = longitude
    items['longitude'] = longitude
    items['address'] = address
    
    session['address'] = address
    session['latitude'] = latitude
    session['longitude'] = longitude

    return jsonify(items)


def reverse_geocode(lat, lon):
    url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
    
    params = {
        "coords": f"{lon},{lat}",
        "output": "json",
        "orders": "addr,roadaddr"  # addr(지번 주소), roadaddr(도로명 주소)
    }
    
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NCP_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NCP_CLIENT_SECRET
    }

    response = requests.get(url, params=params, headers=headers)
    result = response.json()
    
    if "results" in result and len(result["results"]) > 0:
        address = result["results"][0]["region"]
        return [address['area'+str(i)]['name'] for i in range(1,5)]
        # return f"{address['area1']['name']},{address['area2']['name']} {address['area3']['name']} {address['area4']['name']}"
    else:
        return "주소를 찾을 수 없습니다."

CHAT_NORMAL = "일반 대화"
CHAT_ASKMORE = "음식점 메뉴 추천 없이 일반 질문"
CHAT_MENURCMD = "음식점 메뉴 추천"
CHAT_MENURCMD_MYCOND = "본인 상태 알림 및 관련 음식점 메뉴 추천"
CHAT_MENURCMD_MYTASTE = "먹고 싶은 음식점 메뉴 설명 및 추천"

CHAT_TYPES = [CHAT_NORMAL, CHAT_ASKMORE, CHAT_MENURCMD, CHAT_MENURCMD_MYCOND, CHAT_MENURCMD_MYTASTE]

@app.route("/aiagent")
def aiagent():
    global messages
    messages = []
    messages.append({"role": "system", "content": "너는 음식 메뉴를 추천하는 AI야."})
    return render_template('aiagent.html')

def classify_request(user_input):
    string_types = "".join([f"- {item}\n" for item in CHAT_TYPES])
    prompt = f"""
    다음 문장이 어떤 유형인지 분류해줘. 가능한 카테고리는 다음과 같아:
    {string_types}
    
    문장: "{user_input}"
    
    답변 형식은 반드시 다음과 같이 해줘:
    
    분류: [카테고리명]
    
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "너는 입력된 문장을 카테고리로 분류하는 AI야."},
                  {"role": "user", "content": prompt}],
        temperature=0  # 일관된 응답을 위해 0으로 설정
    )

    # 응답에서 카테고리 추출
    result_text = response.choices[0].message.content
    category = result_text.split("분류: ")[-1].strip()
    print(category)
    
    return category

def extract_menus_from_text(text):
    prompt = f"""
    다음 문장을 읽고 문장에 존재하는 재료로 이루어진 음식 메뉴 Top 5를 추천해줘. 
    일반 음식점에서 팔지 않는 재료는 메뉴에서 제외해줘.
    차는 찻집으로 바꿔줘.
    
    =======================================================
    문장: "{text}"
    =======================================================
    답변 형식은 반드시 다음과 같이 해줘:
    
    메뉴1,메뉴2,메뉴3,메뉴4,메뉴5
    
    """

    rag = RAG(RAG.INGREDIENTS)
    rag.load_vector_index()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "너는 입력된 문장에서 추천하는 메뉴나 먹기 좋은 메뉴를 제안하는 AI야."},
                  {"role": "system", "content": "고유대명사는 제외하고 일반적인 메뉴로만 대답하고, 답변 형식은 반드시 다음과 같이 해줘: 메뉴1,메뉴2,메뉴3,메뉴4,메뉴5"},
                  {"role": "user", "content": rag.search_and_wrap(prompt)}],
        temperature=0  # 일관된 응답을 위해 0으로 설정
    )

    # 응답에서 카테고리 추출
    result_text = response.choices[0].message.content
    menus = result_text.split(",")
        
    return menus

@app.route("/chat", methods=["POST"])
def chat():
    if session['address'] == None or session['address'] == "":
        return jsonify({"reply": "주소 정보가 없습니다.", "menus": "", "link_exist": False, "category": CHAT_NORMAL})

    user_message = request.json["message"]
    global messages
    rag = RAG(RAG.HEALTH)
    rag.load_vector_index()
    category = classify_request(user_message)
    print("대화 카테고리:", category)
    if category == CHAT_MENURCMD_MYCOND:
        messages.append({"role": "user", "content": rag.search_and_wrap(user_message)})
    else:
        messages.append({"role": "user", "content": user_message})
        
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = f"오류 발생: {str(e)}"

    link_exist = False
    if category in [CHAT_MENURCMD, CHAT_MENURCMD_MYTASTE, CHAT_MENURCMD_MYCOND]:
        menus = extract_menus_from_text(bot_reply)
        link_exist = True
    else:
        menus = []
        link_exist = False
    print(menus)
    if len(menus) > 0:
        add_str = "[{}]".format(",".join(menus))

    items = search_store(session['address'], menus_str=",".join(menus))
    print("가게 정보", items)
    
    return jsonify({"reply": bot_reply + "추천하는 메뉴: " + add_str,
                    "menus": ",".join(menus),
                    "stores": items[:3],
                    "link_exist": link_exist,
                    "category": category})

if __name__ == "__main__":
    app.run(debug=True)
