
import pandas as pd
import time
from core.data_utils import get_klines
from telegram_bot import send_telegram

LOG_FILE = "performance_log.csv"

def check_signals():
    try:
        df = pd.read_csv(LOG_FILE)
    except FileNotFoundError:
        print("Aucun journal de signal détecté.")
        return

    updated = False
    for i, row in df.iterrows():
        if row['result'] != "pending":
            continue

        symbol = row['symbol']
        entry = float(row['entry'])
        tp = float(row['tp'])
        sl = float(row['sl'])
        direction = row['direction']

        df_price = get_klines(symbol, interval="1m", limit=20)
        if df_price.empty:
            continue

        highs = df_price['high']
        lows = df_price['low']
        last_price = df_price['close'].iloc[-1]

        hit_tp = (highs.max() >= tp) if direction == "LONG" else (lows.min() <= tp)
        hit_sl = (lows.min() <= sl) if direction == "LONG" else (highs.max() >= sl)

        if hit_tp:
            df.at[i, "result"] = "win"
            df.at[i, "pnl"] = tp - entry if direction == "LONG" else entry - tp
            msg = f"✅ TP atteint sur {symbol} ({direction})\nEntrée: {entry:.4f} → TP: {tp:.4f}"
            send_telegram(msg)
            updated = True
        elif hit_sl:
            df.at[i, "result"] = "loss"
            df.at[i, "pnl"] = sl - entry if direction == "LONG" else entry - sl
            msg = f"❌ SL touché sur {symbol} ({direction})\nEntrée: {entry:.4f} → SL: {sl:.4f}"
            send_telegram(msg)
            updated = True

    if updated:
        df.to_csv(LOG_FILE, index=False)
        print("📈 Résultats mis à jour.")

if __name__ == "__main__":
    while True:
        print("🔎 Suivi des signaux...")
        check_signals()
        time.sleep(60)
