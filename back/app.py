from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)
CORS(app)  # Vite 프론트엔드와 CORS 문제 방지

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY) 

@app.route("/")
def home():
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