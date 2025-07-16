import os
import requests

# URL de l'API Binance Futures
BINANCE_API_URL    = "https://fapi.binance.com"

# Clés via variables d'environnement
BINANCE_API_KEY    = os.getenv("BINANCE_API_KEY", "")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")
TELEGRAM_TOKEN     = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

def get_top_usdt_futures(n: int = 400) -> list[str]:
    """
    Récupère les n contrats USDT-M PERP les plus liquides (quoteVolume 24h).
    """
    url  = f"{BINANCE_API_URL}/fapi/v1/ticker/24hr"
    resp = requests.get(url, headers={"X-MBX-APIKEY": BINANCE_API_KEY})
    data = resp.json()

    # Sécurité : on s'assure bien d'avoir une liste
    if not isinstance(data, list):
        raise RuntimeError(f"Réponse inattendue de Binance: {type(data)} – {data}")

    # Filtrer et trier
    usdt_pairs = [
        d for d in data
        if isinstance(d, dict) and d.get("symbol", "").endswith("USDT")
    ]
    usdt_pairs.sort(key=lambda d: float(d.get("quoteVolume", 0)), reverse=True)

    # On renvoie juste les symboles
    return [d["symbol"] for d in usdt_pairs[:n]]

# Chargement en import
SYMBOLS_TO_SCAN = get_top_usdt_futures()

