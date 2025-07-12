import pandas as pd
import requests

BASE_URL = "https://fapi.binance.com"

def get_ohlcv(symbol, interval="4h", limit=100):
    """
    Récupère les bougies futures USDT-M perpétuels via REST.
    """
    url = f"{BASE_URL}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    data = requests.get(url, params=params).json()
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    df = df[["open_time", "open", "high", "low", "close", "volume"]]
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
    return df

def get_last_price(symbol):
    """
    Récupère le dernier prix futures via REST.
    """
    url = f"{BASE_URL}/fapi/v1/ticker/price"
    params = {"symbol": symbol}
    data = requests.get(url, params=params).json()
    return float(data["price"])
