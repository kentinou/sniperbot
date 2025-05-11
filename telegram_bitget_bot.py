from flask import Flask, request
import requests
import os
import threading

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
PASSPHRASE = os.environ.get("PASSPHRASE")

CAPITAL = float(os.environ.get("CAPITAL", 100))
RISK_PER_TRADE = float(os.environ.get("RISK_PER_TRADE", 0.02))

active = False

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "✅ Serveur actif", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    global active
    data = request.get_json()
    print("📩 Webhook reçu:", data)

    if "message" in data:
        msg = data["message"]
        text = msg.get("text", "").strip().lower()

        if text == "/start":
            if not active:
                active = True
                send_message("🚀 SniperBot démarré.")
                threading.Thread(target=scan_and_trade, daemon=True).start()
            else:
                send_message("✅ SniperBot déjà actif.")

        elif text == "/stop":
            active = False
            send_message("🛑 SniperBot arrêté.")

        elif text == "/ping":
            send_message("🏓 Pong ! Le bot est en ligne.")

        elif "strat" in text:
            send_message("📘 Stratégie : Scalping intelligent sur BTC. Risque : 2%, levier max 5x, retracements parfaits. Trade dès qu’un signal fort est détecté.")

    return "OK", 200

def scan_and_trade():
    import time
    while active:
        # --- Exemple de détection de signal ---
        opportunity = detect_signal()
        if opportunity:
            send_message("📈 Signal détecté sur BTC/USDT ! Ouverture de position en scalping..")
            success = place_order()
            if success:
                send_message("✅ Trade exécuté ✅")
            else:
                send_message("⚠️ Échec de l’exécution.")
        time.sleep(30)  # Attente avant nouveau scan

def detect_signal():
    # Simule une détection d’opportunité
    import random
    return random.random() > 0.8

def place_order():
    # Simule une exécution sur Bitget
    # TODO : remplacer par appel réel API Bitget via signature
    print("💼 Envoi ordre à Bitget (simulation)")
    return True

if __name__ == "__main__":
    print("🚀 Serveur webhook lancé.")
    app.run(host="0.0.0.0", port=8080)
