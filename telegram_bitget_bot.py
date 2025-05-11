import os
import requests
from flask import Flask, request
from dotenv import load_dotenv
from python_bitget.client import Client

# Charger les variables d'environnement
load_dotenv()

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
PASSPHRASE = os.getenv("BITGET_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialisation du client Bitget
client = Client(api_key=API_KEY, api_secret=API_SECRET, passphrase=PASSPHRASE)

# Configuration Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '🚀 SuperBot is Live!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 Webhook reçu:", data)

    if "message" in data:
        message_text = data["message"].get("text", "")
        if message_text == "/start":
            send_telegram("✅ Bot opérationnel sur Render.")
        elif "buy" in message_text.lower():
            send_telegram("🟢 Signal d’achat reçu ! (simulation)")
        elif "sell" in message_text.lower():
            send_telegram("🔴 Signal de vente reçu ! (simulation)")

    return "OK", 200

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        response = requests.post(url, json=payload)
        print("📤 Message Telegram envoyé.")
    except Exception as e:
        print("❌ Erreur envoi Telegram:", e)

if __name__ == '__main__':
    print("🚀 Serveur webhook lancé.")
    app.run(host='0.0.0.0', port=8080)
