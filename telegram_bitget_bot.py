from flask import Flask, request
import os
import requests
from dotenv import load_dotenv
from bitget.mix.order import OrderApi
from bitget.mix.market import MarketApi

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Bitget API
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

# Initialisation des APIs Bitget
order_api = OrderApi(api_key=BITGET_API_KEY, secret_key=BITGET_API_SECRET, passphrase=BITGET_API_PASSPHRASE)
market_api = MarketApi()

def send_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "Bot OK ✅", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "No message", 400

    text = data["message"].get("text", "").strip().lower()
    chat_id = data["message"]["chat"]["id"]

    if text == "/start":
        send_message("🚀 SniperBot démarré.")
        return "Started", 200

    elif text.startswith("buy"):
        symbol = "BTCUSDT_UMCBL"
        size = 0.01  # adapte selon ton capital
        send_message(f"📈 Signal détecté sur {symbol} ! Ouverture de position...")
        try:
            result = order_api.place_order(
                symbol=symbol,
                marginCoin="USDT",
                side="open_long",
                orderType="market",
                size=size
            )
            send_message(f"✅ Ordre exécuté: {result}")
        except Exception as e:
            send_message(f"❌ Erreur Bitget: {e}")
        return "Order sent", 200

    return "No action", 200

if __name__ == "__main__":
    print("🚀 Serveur webhook lancé.")
    app.run(host="0.0.0.0", port=8080)
