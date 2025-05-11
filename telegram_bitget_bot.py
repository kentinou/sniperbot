import os
from flask import Flask, request
import requests
from dotenv import load_dotenv
from python_bitget.client import Client

load_dotenv()

app = Flask(__name__)

# Chargement des variables d'environnement
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

client = Client(api_key=API_KEY, api_secret=API_SECRET, passphrase=PASSPHRASE)

def envoyer_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erreur envoi Telegram: {e}")

@app.route('/')
def home():
    return 'Bot Bitget actif'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Webhook reçu:", data)

    if 'message' in data and 'text' in data['message']:
        text = data['message']['text']
        if "/start" in text:
            envoyer_telegram("✅ Bot actif et prêt à trader sur Bitget !")
        elif "Signal détecté" in text and "BTC/USDT" in text:
            envoyer_telegram("📈 Signal détecté, tentative d'ouverture d'un trade BTC/USDT...")

            try:
                response = client.mix_place_order(
                    symbol="BTCUSDT_UMCBL",
                    marginCoin="USDT",
                    side="open_long",
                    orderType="market",
                    size="0.01",
                    leverage="5"
                )
                print(response)
                envoyer_telegram("✅ Trade ouvert avec succès !")
            except Exception as e:
                print(f"Erreur ouverture trade : {e}")
                envoyer_telegram(f"❌ Erreur ouverture trade : {e}")

    return "OK", 200

if __name__ == '__main__':
    print("🚀 Serveur webhook lancé.")
    app.run(host='0.0.0.0', port=8080)
