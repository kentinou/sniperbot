
import os
import time
import hmac
import hashlib
import base64
import requests
import json

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")
BASE_URL = "https://api.bitget.com"

headers = {
    "Content-Type": "application/json",
    "ACCESS-KEY": API_KEY,
    "ACCESS-PASSPHRASE": PASSPHRASE
}

def sign_request(timestamp, method, request_path, body=""):
    message = f"{timestamp}{method}{request_path}{body}"
    mac = hmac.new(bytes(API_SECRET, encoding='utf8'), bytes(message, encoding='utf8'), digestmod=hashlib.sha256)
    return base64.b64encode(mac.digest()).decode()

def place_order():
    timestamp = str(int(time.time() * 1000))
    path = "/api/mix/v1/order/placeOrder"
    url = BASE_URL + path

    order_data = {
        "symbol": "BTCUSDT",
        "marginCoin": "USDT",
        "size": "0.01",
        "side": "open_long",
        "orderType": "market",
        "leverage": "5"
    }

    body = json.dumps(order_data)
    headers.update({
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-SIGN": sign_request(timestamp, "POST", path, body)
    })

    response = requests.post(url, headers=headers, data=body)
    print("📥 Order Response:", response.json())

def cancel_all_orders():
    print("🛑 Annulation des ordres (à implémenter si nécessaire)")
