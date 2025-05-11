
import os
from flask import Flask, request
from dotenv import load_dotenv
from python_bitget.client import Client
from python_bitget.apis.mix import MixOrderApi
import requests

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Récupérer les variables d'environnement
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
CHAT_ID = os.getenv("CHAT_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CAPITAL = float(os.getenv("CAPITAL"))

# Initialiser le client Bitget
client = Client(API_KEY, API_SECRET, PASSPHRASE)
order_api = MixOrderApi(client)

# Fonction d'envoi de message Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

@app.route('/')
def index():
    return "✅ Bot Bitget actif"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"📩 Webhook reçu : {data}")
    send_telegram_message(f"📩 Webhook reçu : {data}")
    
    # Exemple : exécution d'un ordre fictif
    try:
        symbol = data.get("symbol", "BTCUSDT")
        side = data.get("side", "open_long")
        size = float(data.get("size", 0.01))
        marginCoin = data.get("marginCoin", "USDT")
        order_type = "market"

        response = order_api.place_order(
            symbol=symbol,
            marginCoin=marginCoin,
            size=size,
            side=side,
            orderType=order_type
        )
        send_telegram_message(f"✅ Ordre exécuté: {response}")
        return "Ordre placé", 200
    except Exception as e:
        send_telegram_message(f"❌ Erreur lors du placement de l'ordre: {str(e)}")
        return f"Erreur: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
