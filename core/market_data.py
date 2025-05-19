import ccxt

exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})

def get_futures_symbols():
    markets = exchange.load_markets()
    symbols = [s for s in markets if s.endswith("/USDT") and "PERP" in markets[s]['id']]
    return symbols