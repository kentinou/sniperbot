import os
from flask import Flask, request
from dotenv import load_dotenv
from python_bitget.client import Client
from python_bitget.apis.mix import MixOrderApi

# Charger les variables d'environnement
load_dotenv()

# Initialisation de Flask
app = Flask(__name__)

# Récupération des variables d'environnement
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
CHAT_ID = os.getenv("CHAT_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CAPITAL = float(os.getenv("CAPITAL", "100"))

# Initialisation du client Bitget
client = Client(API_KEY, API_SECRET, PASSPHRASE)
order_api = MixOrderApi(client)

@app.route('/')
def index():
    return "✅ Bot Bitget en ligne."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"📩 Webhook reçu: {data}")

    # Exemple : ici tu pourrais déclencher une position sur Bitget via `order_api`
    # Exemple fictif à compléter :
    # result = order_api.place_order(...)
    # print(f"🚀 Trade lancé : {result}")

    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
