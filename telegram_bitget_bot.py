import os
import requests
from flask import Flask, request
from bitget.rest.mix import MixOrderApi, MixMarketApi
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
CAPITAL = float(os.getenv("CAPITAL", "100"))
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", "0.02"))
MAX_SL_COUNT = 5

order_api = MixOrderApi(API_KEY, API_SECRET, PASSPHRASE)
market_api = MixMarketApi(API_KEY, API_SECRET, PASSPHRASE)

bot_active = False
sl_count = 0

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

def get_market_price(symbol):
    try:
        ticker = market_api.get_ticker("umcbl", symbol)
        return float(ticker["data"]["last"])
    except Exception:
        return None

def execute_trade(symbol="BTCUSDT", leverage=5):
    global sl_count
    size = round(CAPITAL * RISK_PER_TRADE * leverage / 100, 2)
    price = get_market_price(symbol)
    if not price:
        send_message("❌ Erreur lors de la récupération du prix.")
        return

    try:
        order = order_api.place_order(
            symbol=symbol,
            marginCoin="USDT",
            size=str(size),
            side="open_long",
            orderType="market",
            price="",
            leverage=str(leverage),
            presetStopLossPrice=str(round(price * 0.99, 2)),
            presetTakeProfitPrice=str(round(price * 1.002, 2))
        )
        send_message(f"✅ Trade exécuté : Scalping {symbol} à {price}")
    except Exception as e:
        sl_count += 1
        send_message(f"❌ Échec de l’ordre : {str(e)}")
        if sl_count >= MAX_SL_COUNT:
            send_message("⚠️ 5 SL consécutifs. Le bot attend un nouveau signal.")
            return

@app.route("/", methods=["GET"])
def home():
    return "✅ Serveur actif.", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    global bot_active
    data = request.get_json(force=True)
    print("📩 Webhook reçu:", data)

    if "message" in data:
        text = data["message"].get("text", "").lower()
        if text == "/start":
            bot_active = True
            send_message("🚀 SniperBot démarré.")
            execute_trade()
        elif text == "/stop":
            bot_active = False
            send_message("🛑 SniperBot arrêté.")
        elif text == "/strat":
            send_message("📋 Stratégie : Scalping, sniper retracements 0.618-0.786, max 2% risk, SL auto, TP rapide.")
        elif text.startswith("buy"):
            if bot_active:
                execute_trade()
        elif text == "/ping":
            send_message("🏓 Pong !")

    return "OK ✅", 200

if __name__ == "__main__":
    print("🚀 Serveur webhook lancé.")
    app.run(host="0.0.0.0", port=8080)
