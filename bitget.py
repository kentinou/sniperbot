import time
import hmac
import hashlib
import requests

class BitgetClient:
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.base_url = "https://api.bitget.com/api"

    def _headers(self, method, path, timestamp, body=""):
        message = f"{timestamp}{method}{path}{body}"
        signature = hmac.new(
            self.api_secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }

    def get_price(self, symbol):
        try:
            url = f"https://api.bitget.com/api/spot/v1/market/ticker?symbol={symbol}"
            res = requests.get(url)
            return res.json()["data"]["last"]
        except:
            return None

    def place_order(self, symbol, side, size, entry, sl, tp):
        print(f"Placer {side.upper()} {symbol} qty={size} entry={entry}")
        return {"symbol": symbol, "side": side, "entry": entry, "tp": tp, "sl": sl}

    def monitor_trade(self, order):
        print(f"Moniteur trade: {order}")
        # Simule un TP ou SL
        time.sleep(5)
        return "tp"
