from flask import Flask, request
import os
import requests
from dotenv import load_dotenv
from bitget.rest_client import RestClient
from bitget.apis.mix.order import OrderApi
from bitget.apis.mix.market import MarketApi

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")
CAPITAL = float(os.getenv("CAPITAL", 150))
SYMBOL = "BTCUSDT_UMCBL"
LEVERAGE = 3
ENTRY_PERCENTAGE = 0.95  # 95% du capital par position
TP_PERCENT = 0.002  # Take profit à +0.2%
SL_PERCENT = 0.002  # Stop loss à -0.2%

client = RestClient(API_KEY, API_SECRET, API_PASSPHRASE, use_server_time=True)
order_api = OrderApi(client)
market_api = MarketApi(client)

is_running = False


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)


def get_price():
    res = market_api.get_market_price(symbol=SYMBOL)
    return float(res['data']['markPrice'])


def place_order():
    entry_price = get_price()
    usdt_amount = CAPITAL * ENTRY_PERCENTAGE
    quantity = round((usdt_amount * LEVERAGE) / entry_price, 4)

    # Crée l'ordre
    try:
        send_message("📈 Signal détecté sur BTC/USDT ! Ouverture de position en scalping...")
        order = order_api.place_order(
            symbol=SYMBOL,
            marginCoin="USDT",
            size=str(quantity),
            side="open_long",
            orderType="market",
            price="",  # non utilisé pour market
            timeInForceValue="normal"
        )
        send_message("✅ Position ouverte (long BTC). Surveillance du TP/SL...")
        monitor_trade(entry_price, quantity)
    except Exception as e:
        send_message(f"❌ Erreur lors de l'ouverture de position : {e}")


def monitor_trade(entry_price, quantity):
    tp_price = entry_price * (1 + TP_PERCENT)
    sl_price = entry_price * (1 - SL_PERCENT)

    while True:
        price = get_price()
        if price >= tp_price:
            close_position(quantity)
            send_message(f"✅ Take Profit atteint à {price:.2f} 🚀")
            break
        elif price <= sl_price:
            close_position(quantity)
            send_message(f"🛑 Stop Loss atteint à {price:.2f} ❌")
            break


def close_position(quantity):
    try:
        order_api.place_order(
            symbol=SYMBOL,
            marginCoin="USDT",
            size=str(quantity),
            side="close_long",
            orderType="market",
            price="",
            timeInForceValue="normal"
        )
    except Exception as e:
        send_message(f"⚠️ Erreur fermeture position : {e}")


@app.route("/webhook", methods=["POST"])
def webhook():
    global is_running
    data = request.json
    message = data.get("message", {})
    text = message.get("text", "")

    if "/start" in text:
        if not is_running:
            is_running = True
            send_message("🚀 SniperBot démarré.")
            place_order()
        else:
            send_message("🤖 Le bot tourne déjà.")
    elif "/stop" in text:
        is_running = False
        send_message("🛑 SniperBot stoppé.")
    elif "/ping" in text:
        send_message("🏓 Pong, le bot est en ligne.")
    elif "/strat" in text:
        send_message("📊 Scalping BTC/USDT, TP 0.2 %, SL 0.2 %, taille ~95 % capital. Répétition en boucle.")

    return "", 200


@app.route("/")
def home():
    return "SniperBot actif", 200


if __name__ == "__main__":
    print("🚀 Serveur webhook lancé.")
    app.run(host="0.0.0.0", port=8080)
