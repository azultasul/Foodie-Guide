from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
import aiagent_model # 기본 llm 사용 + 프롬프트 엔지니어링
import langchain_model # langchain 사용 + 프롬프트 엔지니어링
import langgraph_model # langgraph + reAct agent
import langgraph_react_model # langgraph + reAct agent
from ReActAgent import ReActAgent # langchain의 tools 모듈 사용, ReAct agent 구현
load_dotenv() 

app = Flask(__name__)
CORS(app)  # Vite 프론트엔드와 CORS 문제 방지

# chatbot-llm 추가
@app.route("/api/aiagent", methods=["POST"])
def aiagent():
    user_message = request.json.get("message")
    message_list = request.json.get("messageList")
    # data = aiagent_model.chat(user_message, message_list)
    # data = langchain_model.chat(user_message, message_list)
    data = langgraph_model.chat(user_message, message_list)
    # data = langgraph_react_model.chat(user_message, message_list)
    
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)