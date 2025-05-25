
import requests
import pandas as pd

def get_symbols():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    data = requests.get(url).json()
    return [s["symbol"] for s in data["symbols"] if s["contractType"] == "PERPETUAL" and s["quoteAsset"] == "USDT"]

def get_klines(symbol, interval="5m", limit=100):
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    if response.status_code != 200:
        return pd.DataFrame()
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df
