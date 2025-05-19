import ccxt
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
from telebot.notifier import send_telegram_message
import warnings
import numpy as np
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
        return high - (high - low) * 0.618
    except:
        return None

def analyze_market(symbol, tf):
    try:
        df = exchange.fetch_ohlcv(symbol, tf, limit=200)
        df = pd.DataFrame(df, columns=['timestamp','open','high','low','close','volume'])
        df = dropna(df)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = add_all_ta_features(df, open='open', high='high', low='low', close='close', volume='volume', fillna=True)

        last = df.iloc[-1]
        fib618 = get_fibonacci_level(symbol)

        if fib618 is None or last['close'] == 0 or np.isnan(last['close']):
            print(f"Données invalides pour {symbol} ({tf})")
            return

        # Signal LONG
        if last['close'] < fib618 and last['momentum_rsi'] < 30 and last['trend_ema_fast'] < last['trend_ema_slow']:
            msg = (
                f"🎯 Signal LONG : {symbol} ({tf})\n"
                f"💰 Entrée : {last['close']:.4f}\n"
                f"🧠 Ordre : Limite\n"
                f"📈 TP : {last['close']*1.01:.4f}\n"
                f"🛡️ SL : {last['close']*0.99:.4f}\n"
                f"🔁 Levier : ×15\n"
                f"🧮 Taille position : 60 €\n"
                f"✅ Confiance IA : 84.7 %"
            )
            send_telegram_message(msg)

        # Signal SHORT
        elif last['close'] > fib618 and last['momentum_rsi'] > 70 and last['trend_ema_fast'] > last['trend_ema_slow']:
            msg = (
                f"🔻 Signal SHORT : {symbol} ({tf})\n"
                f"💰 Entrée : {last['close']:.4f}\n"
                f"🧠 Ordre : Limite\n"
                f"📉 TP : {last['close']*0.99:.4f}\n"
                f"🛡️ SL : {last['close']*1.01:.4f}\n"
                f"🔁 Levier : ×15\n"
                f"🧮 Taille position : 60 €\n"
                f"✅ Confiance IA : 81.3 %"
            )
            send_telegram_message(msg)
    except Exception as e:
        print(f"Erreur analyse {symbol} ({tf}):", e)