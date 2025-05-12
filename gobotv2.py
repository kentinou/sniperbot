import os
import time
import requests
from bitget.spot.spot_trade import SpotTrade
from bitget.spot.spot_market import SpotMarket
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
PASSPHRASE = os.getenv("BITGET_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

trade_client = SpotTrade(API_KEY, API_SECRET, PASSPHRASE)
market_client = SpotMarket()

symbol = "BTCUSDT"
capital_usdt = 200
risk_percent = 2
leverage = 5

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Erreur Telegram:", e)

def get_price():
    ticker = market_client.get_ticker(symbol)
    return float(ticker['data']['close'])

def place_trade():
    entry_price = get_price()
    trade_size = (capital_usdt * risk_percent / 100) * leverage / entry_price
    trade_size = round(trade_size, 5)

    send_telegram_message(f"[GOBOTV2] Achat BTCUSDT : {trade_size} BTC @ {entry_price}$")

    order = trade_client.place_order(symbol, "buy", "market", size=str(trade_size))
    time.sleep(5)

    while True:
        current_price = get_price()
        if current_price > entry_price * 1.001:
            trade_client.place_order(symbol, "sell", "market", size=str(trade_size))
            send_telegram_message(f"[GOBOTV2] Fermeture BTCUSDT : {trade_size} BTC @ {current_price}$")
            break
        time.sleep(2)

def main():
    while True:
        try:
            place_trade()
            time.sleep(10)
        except Exception as e:
            send_telegram_message(f"[ERREUR GOBOTV2] {str(e)}")
            time.sleep(30)

if __name__ == "__main__":
    send_telegram_message("[GOBOTV2] Bot démarré avec succès.")
    main()
