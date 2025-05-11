import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    if BOT_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text})

@app.route("/", methods=["GET"])
def home():
    return "Bot test actif ✅", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Reçu via webhook:", data)

    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        if text.strip().lower() == "/ping":
            send_message("pong ✅")
        else:
            send_message(f"👋 Reçu: {text}")
    return "OK", 200

if __name__ == "__main__":
    print("🚀 Bot de test lancé.")
    app.run(host="0.0.0.0", port=8080)
