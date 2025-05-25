
import time
import pandas as pd
from binance.client import Client
from signal_generator_pro import analyse_signal
import requests

API_KEY = ""
API_SECRET = ""
TG_TOKEN = "8093249984:AAEysv-W_6NSF64tbeKjk8stqIKInBcX_7w"
CHAT_ID = "7290247547"

client = Client(API_KEY, API_SECRET)

def get_klines(symbol, interval, limit=500):
    try:
        data = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                         'close_time', 'qav', 'trades', 'tbav', 'tqav', 'ignore'])
        df[['open','high','low','close','volume']] = df[['open','high','low','close','volume']].astype(float)
        return df
    except Exception as e:
        print(f"[ERROR] get_klines {symbol} {interval} → {e}")
        return None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"[ERROR] Telegram API response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Sending Telegram message → {e}")

def run():
    while True:
        try:
            symbols = [s['symbol'] for s in client.futures_exchange_info()['symbols']
                       if s['contractType'] == 'PERPETUAL' and s['quoteAsset'] == 'USDT']
            for symbol in symbols:
                print(f"🔍 Analyse de {symbol}...")
                df_1m = get_klines(symbol, '1M', 30)
                df_1h = get_klines(symbol, '1h', 100)
                if df_1m is not None and df_1h is not None:
                    msg = analyse_signal(df_1h, df_1m, symbol)
                    if msg:
                        print(f"✅ SIGNAL sur {symbol} : {msg.splitlines()[0]}")  # affiche juste la première ligne du message
                        send_telegram(msg)
                    else:
                        print("→ Pas de signal")
                else:
                    print(f"[WARN] Données manquantes pour {symbol}")
            time.sleep(30)
        except Exception as e:
            print(f"[ERROR] Boucle principale → {e}")
            time.sleep(10)

if __name__ == "__main__":
    run()
