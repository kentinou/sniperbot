import requests

def get_top_usdt_futures(limit=400):
    """
    Récupère les symbols USDT-M perpétuels triés par volume 24 h via REST.
    """
    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    data = requests.get(url).json()
    usdt = [d for d in data if d["symbol"].endswith("USDT")]
    usdt.sort(key=lambda x: float(x["quoteVolume"]), reverse=True)
    return [d["symbol"] for d in usdt[:limit]]

SYMBOLS_TO_SCAN = get_top_usdt_futures(400)
