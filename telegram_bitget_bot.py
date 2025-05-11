import os
import time
import requests
from dotenv import load_dotenv
from bitget.client import Client  
from flask import Flask, request

load_dotenv()

# === CONFIGURATION ===
API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = Flask(__name__)

# === INITIALISATION CLIENT ===
client = Client(api_key=API_KEY, api_secret=API_SECRET, passphrase=PASSPHRASE)

# === ENVOI DE MESSAGE TELEGRAM ===
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erreur Telegram: {e}")

# === STRAT DE SCALPING BTC/USDT ===
def sniper_btc():
    symbol = "BTCUSDT_UMCBL"
    try:
        market = client.mix_get_market_price(symbol=symbol)
        mark_price = float(market["data"]["markPrice"])
        send_telegram(f"📈 Signal détecté sur BTC/USDT ! Prix: {mark_price} — Ouverture de position en scalping...")

        # PARAMÈTRES DE L'ORDRE
        size = 0.01  # Adapter selon ton capital
        order = client.mix_place_order(
            symbol=symbol,
            marginCoin="USDT",
            side="open_long",
            orderType="market",
            size=str(size),
            price="",  # vide car market
            leverage="5"
        )

        send_telegram(f"✅ Position ouverte : {order}")
    except Exception as e:
        send_telegram(f"❌ Erreur sur sniper BTC : {e}")
        print("Erreur:", e)

# === ROUTE FLASK POUR DÉCLENCHER /start
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        msg = data["message"]
        text = msg.get("text", "")
        if text == "/start":
            send_telegram("✅ SniperBot actif.")
            sniper_btc()
    return "", 200

# === LANCEMENT SERVEUR
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
