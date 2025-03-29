from flask import Flask, jsonify, request, render_template, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
import aiagent_model
load_dotenv() 

app = Flask(__name__)
app.secret_key = os.urandom(24) # 비밀 키 설정 (세션을 안전하게 사용하기 위해 필요)
CORS(app)  # Vite 프론트엔드와 CORS 문제 방지

# chatbot-llm 추가
@app.route("/api/aiagent", methods=["POST"])
def aiagent():
    user_message = request.json["message"]
    data = aiagent_model.chat(user_message, session)
    
    return jsonify(data)

@app.route("/api/aiagent/reset", methods=["GET"])
def aiagent_reset():
    session['messages'] = None
    return True

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # 환경 변수 PORT가 없으면 기본값 5000 사용
    app.run(host="0.0.0.0", port=port, debug=True)