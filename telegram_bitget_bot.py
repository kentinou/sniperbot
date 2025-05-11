import os
import time
import threading
import requests
from flask import Flask, request
from bitget import BitgetClient

app = Flask(__name__)

# ENV VARS
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
CAPITAL = float(os.getenv("CAPITAL", "150"))
RISK = float(os.getenv("RISK_PER_TRADE", "0.02"))
MAX_LOSSES = 5

# GLOBALS
client = BitgetClient(API_KEY, API_SECRET, PASSPHRASE)
enabled = False
consecutive_losses = 0
targets = ["BTCUSDT", "XRPUSDT", "SOLUSDT"]

def send_msg(txt):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
            "chat_id": CHAT_ID, "text": txt
        })
    except Exception as e:
        print("Telegram error:", e)

@app.route("/", methods=["GET"])
def root():
    return "SniperBot actif ✅", 200

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    global enabled
    data = request.get_json()
    if "message" in data:
        msg = data["message"]
        chat_id = str(msg["chat"]["id"])
        text = msg.get("text", "").strip().lower()

        if chat_id != str(CHAT_ID):
            return "Unauthorized", 403

        if text == "/start":
            enabled = True
            send_msg("🚀 Bot activé. Analyse des marchés en cours...")
        elif text == "/stop":
            enabled = False
            send_msg("🛑 Bot désactivé manuellement.")
        else:
            send_msg("Commande inconnue. Utilise /start ou /stop")
    return "ok", 200

def check_signal(symbol):
    try:
        price = float(client.get_price(symbol))
        return "buy" if int(price) % 7 == 0 else None
    except:
        return None

def trade_loop():
    global consecutive_losses, enabled
    while True:
        if not enabled or consecutive_losses >= MAX_LOSSES:
            time.sleep(30)
            continue

        for symbol in targets:
            signal = check_signal(symbol)
            if not signal:
                continue

            try:
                price = float(client.get_price(symbol))
                qty = round((CAPITAL * RISK * 5) / price, 3)
                sl = round(price * 0.995, 2)
                tp = round(price * 1.003, 2)

                order = client.place_order(symbol, signal, qty, price, sl, tp)
                if order:
                    send_msg(f"🎯 {symbol} {signal.upper()} lancé à {price}\nTP: {tp} / SL: {sl}")
                    result = client.monitor_trade(order)
                    if result == "tp":
                        send_msg("✅ TP atteint.")
                        consecutive_losses = 0
                    elif result == "sl":
                        send_msg("💥 SL touché.")
                        consecutive_losses += 1
            except Exception as e:
                print(f"Erreur {symbol}:", e)
        time.sleep(60)

if __name__ == "__main__":
    send_msg("🤖 SniperBot prêt. En attente de /start.")
    threading.Thread(target=trade_loop).start()
    app.run(host="0.0.0.0", port=8080)
