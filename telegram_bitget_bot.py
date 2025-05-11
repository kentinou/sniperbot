import os
from flask import Flask, request
from dotenv import load_dotenv
from python_bitget.client import Client
from python_bitget.apis.mix import MixOrderApi

load_dotenv()

app = Flask(__name__)

# ENV VARS
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
CHAT_ID = os.getenv("CHAT_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CAPITAL = float(os.getenv("CAPITAL"))

# Bitget client setup
client = Client(API_KEY, API_SECRET, PASSPHRASE)
order_api = MixOrderApi(client)

@app.route('/')
def index():
    return "✅ Bot Bitget en ligne."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"📩 Webhook reçu: {data}")
    # Tu peux traiter le contenu ici et lancer une position via `order_api`
    return '', 200

if __name__ == '__main__':
    print("🚀 Serveur webhook lancé sur port 8080")
    app.run(host='0.0.0.0', port=8080)
