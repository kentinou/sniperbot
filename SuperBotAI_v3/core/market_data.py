import ccxt

exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})

def get_futures_symbols():
    markets = exchange.load_markets()
    symbols = []
    for s in markets:
        market = markets[s]
        if (
            market.get('contract', False)
            and market['linear']
            and market['quote'] == 'USDT'
            and market['active']
        ):
            symbols.append(market['symbol'])
    return symbols[:100]  # Limite au top 100