import os
from flask import Flask, request
from dotenv import load_dotenv
from bitget.client import Client
from bitget.apis.mix import MixOrderApi

load_dotenv()

app = Flask(__name__)

# 🔐 Variables d'environnement
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
CHAT_ID = os.getenv("CHAT_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CAPITAL = float(os.getenv("CAPITAL"))

# ✅ Initialisation Bitget
client = Client(API_KEY, API_SECRET, PASSPHRASE)
order_api = MixOrderApi(client)

@app.route('/')
def index():
    return "✅ Bot Bitget en ligne."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"📩 Webhook reçu: {data}")
    
    # Tu peux traiter ici les signaux et déclencher un ordre Bitget
    # Exemple : order_api.place_order(...)

    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
