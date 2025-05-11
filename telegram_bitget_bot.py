
from flask import Flask, request
import os
import requests
import json
from bitget import place_order, cancel_all_orders

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = Flask(__name__)

is_running = False
loss_streak = 0

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "🤖 Serveur actif", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    global is_running, loss_streak

    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        text = data["message"]["text"]
        if text == "/start":
            if not is_running:
                is_running = True
                send_message("🚀 SniperBot démarré.")
                place_order()
            else:
                send_message("🚀 SniperBot déjà actif.")
        elif text == "/stop":
            is_running = False
            cancel_all_orders()
            send_message("🛑 SniperBot arrêté.")
    return "OK", 200

if __name__ == "__main__":
    send_message("🤖 SniperBot prêt. En attente de /start.")
    app.run(host="0.0.0.0", port=8080)
