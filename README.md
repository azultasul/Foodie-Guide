# 📍 Foodie Guide

### **RAG + AI 에이전트 기반의 식당 추천 챗봇 서비스**

### [ 프로젝트 설명 ]

딥러닝 프로젝트 | 개발 기간: 2주 | 개발 인원: 2명(선하라, 유다솔)

- OpenAI의 **ChatGPT**(gpt-3.5-turbo)를 기반으로 한 **챗봇** 웹 서비스입니다.
- 사용자의 건강 상태와 기호를 반영하여 음식 메뉴를 추천하고, 사용자 위치를 기반으로 해당 메뉴를 판매하는 식당을 안내합니다.
- 건강 데이터와 음식 재료 데이터를 활용해 **Vector DB**를 구축하고 **RAG**를 적용하여 LLM의 환각 문제를 최소화했습니다.
- **Prompt Engineering** 기법을 적용하여 서비스 최적화를 이루고자 했습니다.
- **LangChain**의 Agent와 Tool 모듈을 활용해 **AI 에이전트** 기반 서비스를 구축했습니다.
- **LangGraph**를 사용해 에이전트의 상태 관리와 플로우 제어를 구현했습니다.
- Flask와 React 기반의 웹 개발 환경을 구축하여 **AI 모델을 실제 서비스에 적용**했습니다. 

# 📍 배포 주소
* https://foodie-guide.duckdns.org/

# 📍 **설치** 및 시작 가이드

### [ Installation ]

```bash
git clone https://github.com/azultasul/Foodie-Guide.git
```

### [ Backend ]

```bash
cd back
pip install -r requirements.txt
python app.py
```

### [ Frontend ]

```bash
cd front
npm install
npm run dev
```

# 📍 기술스택
<img width="600" alt="image" src="https://github.com/user-attachments/assets/762f28d3-d43c-4bef-93d0-601d32ae1ddd" />


# 📍 아키텍쳐 및 폴더 구조

### [ 아키텍쳐 ]
<img width="830" alt="image" src="https://github.com/user-attachments/assets/9d143e4d-b63e-423d-a544-66081bb04d78" />



### [ 폴더 구조 ]

```bash
foodieGuide/
│── back/          # 백엔드(Flask)
│   ├── venv/             # (선택) 가상 환경
│   ├── docs/             # 벡터 DB에 사용되는 txt 파일
│   ├── vector_store/     # FAISS 인덱스 및 chunks 파일
│   ├── app.py            # Flask 메인 서버 파일
│   ├── aiagent_model.py  # LLM 모델
│   ├── RAG.py            # RAG 구현
│   ├── File pre-processing.ipynb    # txt 파일 생성을 위한 전처리
│   ├── build_vector_sotre.py        # 벡터 DB 빌드
│   ├── requirements.txt  # Flask 패키지 리스트
│── front/         # 프론트엔드(React + Vite)
│   ├── public/
│   ├── src/.             # React 코드
│   │   ├── api/          # 딥러닝 모델, naver 등 API 파일
│   │   ├── assets/       # style(css)
│   │   ├── components/   # button, listitem 등 컴포넌트 모음
│   │   ├── hooks/        # 커스텀 훅
│   │   ├── pages/        # 메인 페이지 및 서브 페이지
│   │   ├── App.jsx
│   │   ├── main.jsx
│   ├── index.html        # Vite 엔트리 파일
│   ├── package.json      # Vite 패키지 리스트
│── .gitignore
│── README.md
```

# 📍 주요 기능                                                           

| <img width="500" alt="1" src="https://github.com/user-attachments/assets/0aaf5d65-94ed-465a-8de3-6503478d83b0" /> | <img width="500" alt="2" src="https://github.com/user-attachments/assets/1fafe136-8d3b-4fe5-85f1-0d968c805efc" />                                                               | <img width="500" alt="3" src="https://github.com/user-attachments/assets/af12c1fe-6f64-4c53-9cc2-30c13dabf17d" />    |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| ⭐ **자동 완성 기능** <br />-사전 저장된 사용자 질의문 자동완성         | ⭐ **일반 대화 기능**<br />- 사용자와 챗봇의 일반 대화<br />⭐ **메뉴 추천 대화 기능**<br />- 사용자의 상태 기반의 식단 및 해당 식단을 제공하는 주변 식당 정보 제공 | ⭐ **지도 기능**<br />- 사용자 위치 기반의 식당 정보를 지도로 표시<br />- 지도에 표시된 식당 정보 제공 |
