import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
import threading

# Flask uygulamasını başlat
app = Flask(__name__)

# Kullanıcı API anahtarını girecek
api_key = os.getenv("GOOGLE_API_KEY", "")
if not api_key:
    print("API anahtarı bulunamadı. Lütfen geçerli bir Google Gemini API anahtarı ayarlayın.")
    exit()

genai.configure(api_key=api_key)
conversation_history = []

def chat_with_ai():
    """Kullanıcının tüm mesaj geçmişini göndererek AI'nin anlamasını sağlar."""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        context = "\n".join(conversation_history)
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Bilinmeyen bir hata oluştu: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history
    user_input = request.json.get("user_input", "")
    if not user_input:
        return jsonify({"response": "Lütfen bir mesaj girin."}), 400
    
    conversation_history.append(user_input)
    response = chat_with_ai()
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
