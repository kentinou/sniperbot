import pandas as pd
from core.signal_generator import analyse_signal
from telegram_bot import send_telegram_message
from data_fetcher import get_klines

symbol = "BTCUSDT"

df_5m = get_klines(symbol, interval="5m", limit=100)
df_15m = get_klines(symbol, interval="15m", limit=100)
df_1h = get_klines(symbol, interval="1h", limit=100)
df_1d = get_klines(symbol, interval="1d", limit=100)

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
else:
    message = f"Pas de signal sur {symbol} pour le moment."

send_telegram_message(message)
