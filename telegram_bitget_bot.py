import os
from flask import Flask, request
from dotenv import load_dotenv
from python_bitget.client import Client
from python_bitget.apis.mix import MixOrderApi
import requests

# Charger les variables d’environnement (.env ou Render)
load_dotenv()

# Initialiser Flask
app = Flask(__name__)

# 🔐 Variables d’environnement
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
CHAT_ID = os.getenv("CHAT_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CAPITAL = float(os.getenv("CAPITAL", "60"))

# ✅ Init SDK Bitget
client = Client(API_KEY, API_SECRET, PASSPHRASE)
order_api = MixOrderApi(client)

# 📬 Fonction d'envoi de message Telegram
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("❌ Erreur Telegram :", e)

@app.route('/')
def index():
    return "✅ Bot Bitget en ligne."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 Webhook reçu :", data)

    # Exemple simple : ouverture position long sur BTCUSDT
    try:
        order = {
            "symbol": "BTCUSDT",
            "marginCoin": "USDT",
            "side": "open_long",
            "orderType": "market",
            "size": "0.01",
            "leverage": "5"
        }

        response = order_api.place_order(order)
        print("📤 Réponse Bitget :", response)

        if response.get("code") == "00000":
            send_telegram("✅ Trade exécuté ✅")
        else:
            error = response.get("msg", "Erreur inconnue")
            send_telegram(f"❌ Échec du trade : {error}")

    except Exception as e:
        print("❌ Exception :", e)
        send_telegram(f"❌ Exception : {str(e)}")

    return '', 200

if __name__ == "__main__":
    print("🚀 Serveur webhook lancé.")
    app.run(host='0.0.0.0', port=8080)
