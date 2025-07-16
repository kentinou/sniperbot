import os
import requests

# Clés d'API stockées dans les variables d'environnement
BINANCE_API_KEY    = os.getenv("BINANCE_API_KEY", "")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")
TELEGRAM_TOKEN     = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

def get_top_usdt_futures(n: int = 400) -> list[str]:
    """
    Récupère les n contrats futures USDT-M perpétuels 
    les plus liquides sur Binance (par quoteVolume 24h).
    """
    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    resp = requests.get(url, headers={
        "X-MBX-APIKEY": BINANCE_API_KEY
    })
    data = resp.json()  # liste de dicts

    # Filtrer seulement les symboles en USDT perpétuels
    usdt_list = [
        d for d in data
        if isinstance(d, dict)
        and d.get("symbol", "").endswith("USDT")
        and d.get("contractType", "PERPETUAL") == "PERPETUAL"
    ]

    # Trier par volume échangé (quoteVolume) décroissant
    usdt_list.sort(key=lambda d: float(d.get("quoteVolume", 0)), reverse=True)

    # Extraire uniquement les symboles, limiter à n
    return [d["symbol"] for d in usdt_list[:n]]

# Liste des symboles à scanner
SYMBOLS_TO_SCAN = get_top_usdt_futures(400)
