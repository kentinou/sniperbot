import pandas as pd
from core.signal_generator import analyse_signal
from telegram_bot import send_telegram_message
from data_fetcher import get_klines
from binance.client import Client
import os

API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")
client = Client(API_KEY, API_SECRET)

# 🔄 Récupérer TOUS les symboles de trading actifs
def get_all_symbols():
    exchange_info = client.get_exchange_info()
    symbols = [s['symbol'] for s in exchange_info['symbols']
               if s['status'] == 'TRADING']
    return symbols

symbols = get_all_symbols()

for symbol in symbols:
    try:
        df_5m = get_klines(symbol, interval="5m", limit=100)
        df_15m = get_klines(symbol, interval="15m", limit=100)
        df_1h = get_klines(symbol, interval="1h", limit=100)
        df_1d = get_klines(symbol, interval="1d", limit=100)

        if df_5m.empty or df_15m.empty or df_1h.empty or df_1d.empty:
            continue

        result = analyse_signal(df_5m, df_15m, df_1h, df_1d)

        if result["signal"]:
            message = (
                f"\n🚨 Signal détecté sur {symbol} : {result['signal']}\n"
                f"RSI : {result['rsi']}\n"
                f"Tendance EMA : {result['ema_trend']}\n"
                f"Volume : {result['volume_now']} (moy : {result['volume_ma']})\n"
                f"Pattern bougie : {result['candle_pattern']}\n"
                f"🤖 Confiance IA : {result['confidence']}/100"
            )
            send_telegram_message(message)

    except Exception as e:
        print(f"Erreur avec {symbol} : {e}")
