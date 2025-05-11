import os
import requests
from flask import Flask, request
from dotenv import load_dotenv
from python_bitget.client import Client
import threading
import time

# Charger les variables d'environnement
load_dotenv()

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialiser l'API Bitget
client = Client(API_KEY, API_SECRET, API_PASSPHRASE)
order_api = client.mix_order_api
market_api = client.mix_market_api

# Initialiser Flask
app = Flask(__name__)
bot_active = {"running": False}

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

@app.route("/")
def root():
    return "SniperBot en ligne", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            bot_active["running"] = True
            send_message("🚀 SniperBot démarré.")
            threading.Thread(target=run_bot).start()

        elif text == "/stop":
            bot_active["running"] = False
            send_message("🛑 SniperBot arrêté.")

        elif text == "/ping":
            send_message("🏓 Pong !")

        elif text == "/strat":
            send_message("📊 Stratégie : Scalping BTC avec gestion de capital agressive, TP rapides et levier raisonnable. Stop après 5 pertes consécutives.")

    return "", 200

def run_bot():
    losses = 0
    capital = 150

    while bot_active["running"]:
        try:
            # Lecture du prix BTCUSDT
            ticker = market_api.get_ticker("BTCUSDT_UMCBL")
            price = float(ticker["data"]["last"])

            # Simulation simple d'opportunité
            if price % 5 < 0.1:  # pseudo-signal
                send_message("📈 Signal détecté sur BTC/USDT ! Ouverture de position en scalping...")

                order = order_api.place_order(
                    symbol="BTCUSDT_UMCBL",
                    marginCoin="USDT",
                    side="open_long",
                    size="0.01",
                    price=str(round(price, 2)),
                    orderType="limit",
                    presetTakeProfit=str(round(price * 1.001, 2)),
                    presetStopLoss=str(round(price * 0.999, 2))
                )

                send_message(f"✅ Position ouverte à {price}")
                time.sleep(5)
            else:
                time.sleep(2)

        except Exception as e:
            send_message(f"⚠️ Erreur : {e}")
            time.sleep(10)

if __name__ == "__main__":
    print("🚀 Serveur webhook lancé.")
    app.run(host="0.0.0.0", port=8080)
