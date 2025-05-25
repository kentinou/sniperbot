import requests
import pandas as pd
import time
from datetime import datetime
import telegram

# Configuration Telegram
TELEGRAM_TOKEN = '8093249984:AAEysv-W_6NSF64tbeKjk8stqIKInBcX_7w'
TELEGRAM_CHAT_ID = '7290247547'
bot = telegram.Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def get_binance_klines(symbol, interval, limit=100):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    return df

def get_fibo_points_monthly(df_month):
    # Filtrer les bougies vertes parmi les 20 dernières mensuelles
    green_candles = df_month[df_month['close'] > df_month['open']]
    if len(green_candles) < 2:
        return None, None
    # Prendre la première et la dernière bougie verte sur les 20 dernières
    first_green_candle = green_candles.iloc[0]
    last_green_candle = green_candles.iloc[-1]
    fibo_low = first_green_candle['low']
    fibo_high = last_green_candle['high']
    return fibo_low, fibo_high

def calculate_fibo_levels(low, high):
    diff = high - low
    levels = {
        '1.0': low,
        '0.786': low + 0.214 * diff,
        '0.7': low + 0.3 * diff,
        '0.618': low + 0.382 * diff,
        '0.5': low + 0.5 * diff,
        '0.3': low + 0.7 * diff,
        '0.2': low + 0.8 * diff,
        '0.0': high
    }
    return levels

def is_approaching_level(price_prev, price_current, level_value, tolerance=0.03):
    # Approche du niveau en venant du dessus, tolérance ±3%
    if price_prev > level_value and price_current <= level_value * (1 + tolerance):
        return True
    return False

def main():
    symbols = [
        "BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT", "DOGEUSDT", "SOLUSDT", "PEPEUSDT",
        "BCHUSDT", "LINKUSDT", "ADAUSDT", "DOTUSDT", "MATICUSDT", "UNIUSDT", "AVAXUSDT",
        "ATOMUSDT", "FILUSDT", "TRXUSDT", "XLMUSDT", "NEARUSDT", "ALGOUSDT"
    ]
    interval_month = '1M'
    interval_hour = '1h'

    print("🚀 Bot démarré, analyse en cours...")

    while True:
        try:
            for symbol in symbols:
                print(f"🔍 Analyse de {symbol}...")
                df_month = get_binance_klines(symbol, interval_month, limit=20)
                fibo_low, fibo_high = get_fibo_points_monthly(df_month)
                if fibo_low is None or fibo_high is None:
                    print(f"[{symbol}] Pas assez de bougies vertes mensuelles pour tracer Fibonacci.")
                    continue

                fibo_levels = calculate_fibo_levels(fibo_low, fibo_high)

                df_hour = get_binance_klines(symbol, interval_hour, limit=2)
                price_current = df_hour['close'].iloc[-1]
                price_prev = df_hour['close'].iloc[-2]

                for level_key in ['0.618', '0.7']:
                    level_value = fibo_levels[level_key]
                    if is_approaching_level(price_prev, price_current, level_value):
                        message = (
                            f"📉 LONG {symbol}\n"
                            f"💰 Entrée : {price_current:.6f} USDT\n"
                            f"🎯 TP1 : {fibo_levels['0.5']:.6f}\n"
                            f"🎯 TP2 : {fibo_levels['0.3']:.6f}\n"
                            f"🎯 TP Final : {fibo_levels['0.0']:.6f}\n"
                            f"🛡️ SL : {fibo_levels['1.0']:.6f} (niveau 1.0 du Fibo)\n"
                            f"📉 Approche du niveau {level_key} mensuel (retracement)"
                        )
                        print(f"⚠️ Signal détecté pour {symbol} sur niveau {level_key} !")
                        send_telegram_message(message)
            time.sleep(60)
        except Exception as e:
            print(f"[ERROR] {datetime.now()} - {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
