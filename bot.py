# SuperBot v1 inspiré de la vidéo YouTube "Installer votre robot de trading en Python !"

import time
import hmac
import hashlib
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

API_KEY = os.getenv('BITGET_API_KEY')
API_SECRET = os.getenv('BITGET_API_SECRET')
PASSPHRASE = os.getenv('BITGET_PASSPHRASE')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
BASE_URL = 'https://api.bitget.com'
SYMBOL = 'BTCUSDT_UMCBL'
INTERVAL = '1m'
LEVERAGE = 5
TARGET_PROFIT_USDT = 0.3

# Config des headers Bitget
HEADERS = {
    'ACCESS-KEY': API_KEY,
    'ACCESS-SIGN': '',  # sera rempli dynamiquement
    'ACCESS-TIMESTAMP': '',
    'ACCESS-PASSPHRASE': PASSPHRASE,
    'Content-Type': 'application/json'
}

# Fonction pour signer les requêtes

def sign_request(timestamp, method, request_path, body=''):
    pre_hash = f"{timestamp}{method}{request_path}{body}"
    signature = hmac.new(API_SECRET.encode(), pre_hash.encode(), hashlib.sha256).hexdigest()
    return signature

# Notification Telegram

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': msg}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("[Telegram] Erreur:", e)

# Obtenir les données de prix récentes

def get_latest_price():
    url = f'{BASE_URL}/api/mix/v1/market/ticker?symbol={SYMBOL}'
    response = requests.get(url)
    return float(response.json()['data']['last'])

# Déterminer le signal simple (stratégie Moving Average Cross simplifiée)

def get_trade_signal():
    url = f'{BASE_URL}/api/mix/v1/market/candles?symbol={SYMBOL}&granularity=60&limit=20'
    response = requests.get(url)
    candles = response.json()['data']
    close_prices = [float(candle[4]) for candle in candles]
    ma5 = sum(close_prices[-5:]) / 5
    ma10 = sum(close_prices[-10:]) / 10
    if ma5 > ma10:
        return 'buy'
    elif ma5 < ma10:
        return 'sell'
    return None

# Placer un ordre au marché

def place_order(side, size):
    timestamp = str(int(time.time() * 1000))
    endpoint = '/api/mix/v1/order/place'
    body = {
        "symbol": SYMBOL,
        "marginCoin": "USDT",
        "size": str(size),
        "side": side,
        "orderType": "market",
        "tradeSide": "open",
        "leverage": str(LEVERAGE)
    }
    body_json = json.dumps(body)
    signature = sign_request(timestamp, 'POST', endpoint, body_json)
    headers = HEADERS.copy()
    headers['ACCESS-SIGN'] = signature
    headers['ACCESS-TIMESTAMP'] = timestamp
    response = requests.post(BASE_URL + endpoint, headers=headers, data=body_json)
    send_telegram(f"✅ Ordre {side.upper()} placé. Détails : {response.json()}")
    print(f"[{datetime.now()}] Order placed: {response.json()}")

# Fermer la position ouverte

def close_position():
    timestamp = str(int(time.time() * 1000))
    endpoint = '/api/mix/v1/position/close-position'
    body = {
        "symbol": SYMBOL,
        "marginCoin": "USDT",
        "holdSide": "long"
    }
    body_json = json.dumps(body)
    signature = sign_request(timestamp, 'POST', endpoint, body_json)
    headers = HEADERS.copy()
    headers['ACCESS-SIGN'] = signature
    headers['ACCESS-TIMESTAMP'] = timestamp
    response = requests.post(BASE_URL + endpoint, headers=headers, data=body_json)
    send_telegram("🔴 Position fermée pour prise de profit")
    print(f"[{datetime.now()}] Position fermée: {response.json()}")

# Bot principal

def run_bot():
    print("--- SuperBot lancé ---")
    send_telegram("🚀 SuperBot lancé avec succès")
    while True:
        try:
            signal = get_trade_signal()
            if signal:
                price = get_latest_price()
                capital = 117
                quantity = round((capital * LEVERAGE) / price, 3)
                place_order(signal, quantity)

                # Attente du profit
                entry_price = price
                while True:
                    time.sleep(5)
                    current_price = get_latest_price()
                    gain = (current_price - entry_price) * quantity if signal == 'buy' else (entry_price - current_price) * quantity
                    if gain >= TARGET_PROFIT_USDT:
                        close_position()
                        break
            else:
                print(f"[{datetime.now()}] Aucun signal, attente...")
        except Exception as e:
            print(f"Erreur: {e}")
            send_telegram(f"❌ Erreur détectée : {e}")
        time.sleep(20)

if __name__ == '__main__':
    run_bot()

