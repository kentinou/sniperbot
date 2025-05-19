from market_data import get_futures_symbols
from signal_generator import analyze_market
from notifier import send_telegram_message
import time

def main():
    send_telegram_message("🚀 SuperBot AI v3 lancé. Analyse multi-timeframe en cours...")
    while True:
        try:
            symbols = get_futures_symbols()
            for symbol in symbols:
                for tf in ['5m', '15m', '1h']:
                    analyze_market(symbol, tf)
                    time.sleep(1)
        except Exception as e:
            send_telegram_message(f"⚠️ Erreur dans la boucle principale : {str(e)}")
            time.sleep(10)

if __name__ == "__main__":
    main()
