import os
import time
import threading
import requests
from flask import Flask
from bitget import BitgetClient

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
CAPITAL = float(os.getenv("CAPITAL", "150"))
RISK_PER_TRADE = 0.02
MAX_CONSECUTIVE_LOSSES = 5

client = BitgetClient(API_KEY, API_SECRET, PASSPHRASE)
consecutive_losses = 0

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        res = requests.post(url, json=data)
        print("✅ Message Telegram:", res.json())
    except Exception as e:
        print("❌ Erreur Telegram:", e)

@app.route("/")
def index():
    return "SniperBot actif 🚀", 200

def check_signal():
    # Placeholder — stratégie simple BTC
    ticker = client.get_price("BTCUSDT")
    if not ticker:
        return None

    price = float(ticker)
    # Simule une condition de scalping : prendre si les 2 dernières minutes sont haussières
    return "buy" if price % 5 < 1 else None

def execute_trade():
    global consecutive_losses
    if consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
        send_message("⛔ Trop de SL consécutifs. Attente nouvelle opportunité.")
        return

    signal = check_signal()
    if not signal:
        return

    risk_amount = CAPITAL * RISK_PER_TRADE
    entry = float(client.get_price("BTCUSDT"))
    qty = round((risk_amount * 5) / entry, 4)  # levier 5

    sl = round(entry * 0.995, 2)
    tp = round(entry * 1.005, 2)

    order = client.place_order("BTCUSDT", signal, qty, entry, sl, tp)
    if order:
        send_message(f"✅ Trade {signal} lancé à {entry}\nTP: {tp}, SL: {sl}")
        status = client.monitor_trade(order)
        if status == "tp":
            send_message("🎯 TP touché !")
            consecutive_losses = 0
        elif status == "sl":
            send_message("💥 SL touché.")
            consecutive_losses += 1

def loop():
    while True:
        try:
            execute_trade()
        except Exception as e:
            print("Erreur trading loop:", e)
        time.sleep(60)

if __name__ == "__main__":
    send_message("🤖 SniperBot lancé et connecté à Bitget")
    threading.Thread(target=loop).start()
    app.run(host="0.0.0.0", port=8080)
