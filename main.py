
from market_data import get_futures_symbols
from signal_generator import analyze_market
import time

def main():
    print("🚀 SuperBot AI lancé sur Render. Analyse en cours...")
    timeframes = ["5m", "15m", "1h"]
    while True:
        symbols = get_futures_symbols()
        for symbol in symbols:
            for tf in timeframes:
                analyze_market(symbol, tf)
        time.sleep(60)

if __name__ == "__main__":
    main()
