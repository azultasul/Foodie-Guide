from flask import Flask, jsonify, request, render_template, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
import aiagent_model
import langchain_model
load_dotenv() 

app = Flask(__name__)
CORS(app)  # Vite 프론트엔드와 CORS 문제 방지

# chatbot-llm 추가
@app.route("/api/aiagent", methods=["POST"])
def aiagent():
    user_message = request.json["message"]
    data = aiagent_model.chat(user_message)
    
    return jsonify(data)

@app.route("/api/aiagent/reset", methods=["GET"])
def aiagent_reset():
    session['messages'] = None
    return True

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)