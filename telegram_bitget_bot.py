import os
import time
import threading
import requests
from flask import Flask, request
from bitget import BitgetClient

app = Flask(__name__)

# Env
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
CAPITAL = float(os.getenv("CAPITAL", "150"))
RISK = float(os.getenv("RISK_PER_TRADE", "0.02"))
MAX_LOSSES = 5

# Initialisation
client = BitgetClient(API_KEY, API_SECRET, PASSPHRASE)
enabled = True
consecutive_losses = 0
targets = ["BTCUSDT", "XRPUSDT", "SOLUSDT"]

# Telegram
def send_msg(txt):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": txt})

@app.route("/")
def home():
    return "SniperBot actif ✅", 200

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    global enabled
    data = request.get_json()
    if "message" in data:
        msg = data["message"]
        text = msg.get("text", "")
        if text == "/stop":
            enabled = False
            send_msg("🛑 Bot stoppé via Telegram.")
    return "ok", 200

# Trading loop
def trade_loop():
    global consecutive_losses, enabled
    while True:
        if not enabled or consecutive_losses >= MAX_LOSSES:
            time.sleep(60)
            continue

        for symbol in targets:
            signal = check_signal(symbol)
            if not signal:
                continue

            price = float(client.get_price(symbol))
            qty = round((CAPITAL * RISK * 5) / price, 3)
            sl = round(price * 0.995, 2)
            tp = round(price * 1.003, 2)

            order = client.place_order(symbol, signal, qty, price, sl, tp)
            if order:
                send_msg(f"🎯 {symbol} {signal.upper()} lancé\nEntrée: {price}\nTP: {tp} / SL: {sl}")
                result = client.monitor_trade(order)
                if result == "tp":
                    send_msg("✅ TP atteint.")
                    consecutive_losses = 0
                elif result == "sl":
                    send_msg("💥 SL touché.")
                    consecutive_losses += 1

        time.sleep(60)

def check_signal(symbol):
    # Placeholder simple : si le prix modulo 7 ≈ 0 → signal
    try:
        price = float(client.get_price(symbol))
        return "buy" if int(price) % 7 == 0 else None
    except:
        return None

if __name__ == "__main__":
    send_msg("🤖 SniperBot lancé et actif (BTC/XRP/SOL)")
    threading.Thread(target=trade_loop).start()
    app.run(host="0.0.0.0", port=8080)
