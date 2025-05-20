import time
import pandas as pd
from core.signal_generator import analyse_signal
from telegram_bot import send_telegram_message
from data_fetcher import get_klines
from binance.client import Client
import os

API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")
client = Client(API_KEY, API_SECRET)

POSITION_SIZE_EUR = 60
LEVERAGE = 15
TP_SL_PERCENT = 0.01
MIN_CONFIDENCE = 75

def format_price(price):
    if price >= 100:
        return f"{price:.2f}"
    elif price >= 1:
        return f"{price:.4f}"
    elif price >= 0.01:
        return f"{price:.6f}"
    else:
        return f"{price:.8f}"

def get_usdt_symbols():
    exchange_info = client.get_exchange_info()
    symbols = [s['symbol'] for s in exchange_info['symbols']
               if s['status'] == 'TRADING' and s['quoteAsset'] == 'USDT']
    return symbols

def scan_all_symbols():
    symbols = get_usdt_symbols()
    for symbol in symbols:
        try:
            print(f"🔎 Analyse de {symbol}")
            df_5m = get_klines(symbol, interval="5m", limit=100)
            df_15m = get_klines(symbol, interval="15m", limit=100)
            df_1h = get_klines(symbol, interval="1h", limit=100)
            df_1d = get_klines(symbol, interval="1d", limit=100)

            if df_5m.empty or df_15m.empty or df_1h.empty or df_1d.empty:
                continue

            avg_volume = df_5m['volume'].tail(20).mean()
            if avg_volume < 100:
                continue

            result = analyse_signal(df_5m, df_15m, df_1h, df_1d)

            if result["signal"] and result["confidence"] >= MIN_CONFIDENCE:
                last_price = df_5m['close'].iloc[-1]
                if last_price == 0:
                    continue

                if result["signal"] == "LONG":
                    entry = last_price
                    tp = entry * (1 + TP_SL_PERCENT)
                    sl = entry * (1 - TP_SL_PERCENT)
                    signal_emoji = "🟢"
                    direction = "LONG"
                else:
                    entry = last_price
                    tp = entry * (1 - TP_SL_PERCENT)
                    sl = entry * (1 + TP_SL_PERCENT)
                    signal_emoji = "🔻"
                    direction = "SHORT"

                message = (
                    f"{signal_emoji} Signal {direction} : {symbol} (15m)\n"
                    f"💰 Entrée : {format_price(entry)}\n"
                    f"{'📈' if direction == 'LONG' else '📉'} TP : {format_price(tp)}\n"
                    f"🛡️ SL : {format_price(sl)}\n"
                    f"🔁 Levier : ×{LEVERAGE}\n"
                    f"🧮 Taille position : {POSITION_SIZE_EUR} €"
                )
                send_telegram_message(message)

        except Exception as e:
            print(f"Erreur avec {symbol} : {e}")

if __name__ == "__main__":
    while True:
        print("\n🔄 Scan lancé...")
        scan_all_symbols()
        print("✅ Scan terminé. Pause 5 min.")
        time.sleep(300)
