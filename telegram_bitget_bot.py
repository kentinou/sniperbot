from flask import Flask, request
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Serveur actif", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📥 Webhook reçu:", data)

    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if text == "/start":
        send_message(chat_id, "🤖 Bot démarré et prêt à trader !")

    return "OK ✅", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    print("📤 Réponse Telegram:", r.json())

if __name__ == "__main__":
    print("🚀 Serveur Flask lancé")
    app.run(host="0.0.0.0", port=8080)
