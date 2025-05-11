from flask import Flask, request
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

started = False

@app.route("/", methods=["GET"])
def home():
    return "✅ Serveur actif", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    global started
    data = request.get_json(force=True)
    print("📩 Webhook reçu:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            if not started:
                started = True
                send_message("🚀 SniperBot démarré. Recherche de trades BTC en cours...")
                # Lancer ici la stratégie de scalping BTC
                simulate_trade_btc()
            else:
                send_message("✅ SniperBot déjà actif.")
    return "OK ✅", 200

def simulate_trade_btc():
    send_message("📈 Signal détecté sur BTC/USDT ! Ouverture de position en scalping...")

if __name__ == "__main__":
    print("🚀 Serveur webhook lancé.")
    app.run(host="0.0.0.0", port=8080)
