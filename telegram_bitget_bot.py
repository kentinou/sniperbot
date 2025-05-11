import os
import time
import requests
from flask import Flask, request
from dotenv import load_dotenv
from bitget.client import Client

load_dotenv()

app = Flask(__name__)

BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

client = Client(
    api_key=BITGET_API_KEY,
    api_secret=BITGET_API_SECRET,
    passphrase=BITGET_PASSPHRASE
)

symbol = "BTCUSDT_UMCBL"
margin_coin = "USDT"
size = "0.01"
leverage = "5"
side = "open_long"  # ou "open_short"
reduce_only = False


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erreur Telegram : {e}")


@app.route('/')
def home():
    return '✅ Bot Bitget en ligne.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Webhook reçu:", data)

    if "text" in data.get("message", {}):
        msg_text = data["message"]["text"]

        if msg_text == "/start":
            send_telegram_message("🤖 Bot Bitget actif et prêt à sniper !")
            return "OK"

        if "Signal détecté" in msg_text:
            try:
                # Exemple : ouverture d'une position long sur BTC
                resp = client.mix_place_order(
                    symbol=symbol,
                    marginCoin=margin_coin,
                    side="open_long",
                    size=size,
                    orderType="market",
                    leverage=leverage
                )
                print("🟢 Trade exécuté :", resp)
                send_telegram_message("✅ Trade exécuté sur Bitget !")
            except Exception as e:
                send_telegram_message(f"❌ Erreur trade : {e}")
                print("❌ Erreur Bitget :", e)

    return "OK"


if __name__ == '__main__':
    print("🚀 Serveur webhook lancé.")
    app.run(host="0.0.0.0", port=8080)
