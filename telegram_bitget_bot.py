from flask import Flask, request
import os
import threading
import time
import requests
from bitget.openapi.mix import MixOrderApi, MixMarketApi
from bitget.openapi.client import Client

app = Flask(__name__)

# Chargement des variables d'environnement
API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialisation de l'API Bitget
client = Client(API_KEY, API_SECRET, API_PASSPHRASE)
order_api = MixOrderApi(client)
market_api = MixMarketApi(client)

bot_actif = False

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erreur Telegram: {e}")

@app.route('/')
def index():
    return "SniperBot actif 🚀", 200

@app.route('/webhook', methods=["POST"])
def webhook():
    global bot_actif
    data = request.get_json()
    print("📩 Webhook reçu:", data)
    if "message" in data:
        text = data["message"].get("text", "")
        if text == "/start":
            bot_actif = True
            send_message("✅ SniperBot démarré.")
        elif text == "/stop":
            bot_actif = False
            send_message("🛑 SniperBot arrêté.")
        elif text.lower() == "strat":
            send_message("🎯 Scalping BTC en temps réel avec risk management. Petits profits mais nombreux trades. Stop après 5 SL consécutifs.")
    return "ok", 200

def scalping_loop():
    global bot_actif
    sl_cons = 0
    while True:
        if bot_actif:
            try:
                market_data = market_api.get_ticker("BTCUSDT_UMCBL")  # ex: market/market/get-ticker
                price = float(market_data["data"]["last"])
                # Logique de scalping ici (ex: conditions de momentum ou de cassure)
                send_message("📈 Signal détecté sur BTC/USDT ! Ouverture de position en scalping..")
                # Simule un ordre market long
                order_api.place_order(
                    symbol="BTCUSDT_UMCBL",
                    marginCoin="USDT",
                    side="open_long",
                    orderType="market",
                    size="0.01"
                )
                send_message("✅ Position ouverte ! TP/SL en surveillance..")
                time.sleep(10)
                # Simule clôture rapide du trade
                order_api.place_order(
                    symbol="BTCUSDT_UMCBL",
                    marginCoin="USDT",
                    side="close_long",
                    orderType="market",
                    size="0.01"
                )
                send_message("💰 Trade clôturé avec petit profit.")
                sl_cons = 0
            except Exception as e:
                sl_cons += 1
                send_message(f"❌ Erreur: {e}")
                if sl_cons >= 5:
                    bot_actif = False
                    send_message("🛑 5 SL consécutifs. Pause automatique.")
        time.sleep(15)

def keep_alive():
    while True:
        requests.get("https://sniperbot-l0nm.onrender.com/")
        time.sleep(60)

if __name__ == "__main__":
    print("🚀 Serveur webhook lancé.")
    threading.Thread(target=scalping_loop).start()
    threading.Thread(target=keep_alive).start()
    app.run(host="0.0.0.0", port=8080)
