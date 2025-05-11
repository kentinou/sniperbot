import os
from flask import Flask, request
from bitget.client import Client
from bitget.apis.mix import MixOrderApi
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load env variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
CHAT_ID = os.getenv("CHAT_ID")
CAPITAL = float(os.getenv("CAPITAL"))
BOT_TOKEN = os.getenv("BOT_TOKEN")

client = Client(API_KEY, API_SECRET, PASSPHRASE)
order_api = MixOrderApi(client)

@app.route('/')
def index():
    return "Bot en ligne."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"📩 Webhook reçu: {data}")
    # Ajoute ici ta logique de traitement des signaux
    return '', 200

if __name__ == '__main__':
    print("🚀 Serveur webhook lancé.")
    app.run(host='0.0.0.0', port=8080)
