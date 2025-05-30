from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
import aiagent_model
import langchain_model
from validators import validate_input
from xss_filter import sanitize_input

load_dotenv() 

app = Flask(__name__)
CORS(app)  # Vite 프론트엔드와 CORS 문제 방지

# chatbot-llm 추가
@app.route("/api/aiagent", methods=["POST"])
def aiagent():
    data = request.get_json()
    user_message = request.json.get("message")
    message_list = request.json.get("messageList")

    # 입력 검증
    validate_error = validate_input(data)
    if validate_error :
        return jsonify({"error": validate_error}), 400

    result = aiagent_model.chat(user_message, message_list)
    # XSS 필터링
    result = sanitize_input(result)

    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
