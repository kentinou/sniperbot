
import ccxt
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
from telebot.notifier import send_telegram_message
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})

def get_fibonacci_level(symbol):
    try:
        df = exchange.fetch_ohlcv(symbol, '1w', limit=100)
        df = pd.DataFrame(df, columns=['timestamp','open','high','low','close','volume'])
        high = df['high'].max()
        low = df['low'].min()
        return high - (high - low) * 0.618, high - (high - low) * 0.382
    except:
        return None, None

def analyze_market(symbol, tf):
    try:
        print(f"Analyse de {symbol} en {tf}")
        df = exchange.fetch_ohlcv(symbol, tf, limit=200)
        df = pd.DataFrame(df, columns=['timestamp','open','high','low','close','volume'])
        df = dropna(df)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = add_all_ta_features(df, open='open', high='high', low='low', close='close', volume='volume', fillna=True)

        last = df.iloc[-1]
        fib618, fib382 = get_fibonacci_level(symbol)

        if fib618 is None:
            return

        price_close = last['close']
        rsi = last['momentum_rsi']
        ema_fast = last['trend_ema_fast']
        ema_slow = last['trend_ema_slow']
        distance = abs(price_close - fib618) / fib618

        print(f"{symbol} {tf} | Close: {price_close:.2f}, Fib: {fib618:.2f}, RSI: {rsi:.2f}, Dist: {distance:.4f}")

        # 🔥 Signal agressif LONG
        if price_close < fib618 and (rsi < 40 or ema_fast < ema_slow) and distance < 0.015:
            msg = (
                f"🎯 SIGNAL AGRESSIF LONG : {symbol} ({tf})\n"
                f"💰 Entrée : {price_close:.2f}\n"
                f"📈 TP : {price_close*1.005:.2f}\n"
                f"🛡️ SL : {price_close*0.995:.2f}\n"
                f"🔁 Levier : ×15\n"
                f"✅ Mode réel"
            )
            send_telegram_message(msg)
            print(f"✅ Signal LONG réel envoyé : {symbol} ({tf})")

        # 🔻 Signal agressif SHORT
        elif price_close > fib618 and (rsi > 60 or ema_fast > ema_slow) and distance < 0.015:
            msg = (
                f"🔻 SIGNAL AGRESSIF SHORT : {symbol} ({tf})\n"
                f"💰 Entrée : {price_close:.2f}\n"
                f"📉 TP : {price_close*0.995:.2f}\n"
                f"🛡️ SL : {price_close*1.005:.2f}\n"
                f"🔁 Levier : ×15\n"
                f"✅ Mode réel"
            )
            send_telegram_message(msg)
            print(f"✅ Signal SHORT réel envoyé : {symbol} ({tf})")

    except Exception as e:
        print(f"Erreur analyse {symbol} ({tf}):", e)
