#!/usr/bin/env python3
import time
import pandas as pd
from binance_api import get_last_price
from telebot import send_signal
from datetime import datetime
from zoneinfo import ZoneInfo

tz = ZoneInfo("Europe/Brussels")
CSV_PATH = "signaux.csv"
POLL_INTERVAL = 60

def main():
    notified = set()
    print(f"[ {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')} ] Monitor démarré, sortie TP/SL ATR", flush=True)
    while True:
        try:
            df = pd.read_csv(CSV_PATH)
        except FileNotFoundError:
            time.sleep(POLL_INTERVAL)
            continue
        open_idx = df[df['status'] == 'open'].index
        for idx in open_idx:
            row = df.loc[idx]
            symbol = row['symbol']
            side = row['side']
            entry = float(row['entry'])
            tp = float(row['tp'])
            sl = float(row['sl'])
            price = get_last_price(symbol)
            now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
            print(f"[ {now} ] Monitoring {symbol}: price={price:.6f}", flush=True)
            if side == 'buy':
                if price >= tp:
                    status = 'win'
                elif price <= sl:
                    status = 'loss'
                else:
                    continue
            else:
                if price <= tp:
                    status = 'win'
                elif price >= sl:
                    status = 'loss'
                else:
                    continue
            exit_price = price
            pnl = ((exit_price - entry) / entry) if side == 'buy' else ((entry - exit_price) / entry)
            df.at[idx, 'exit_price'] = exit_price
            df.at[idx, 'pnl'] = pnl
            df.at[idx, 'status'] = status
            df.to_csv(CSV_PATH, index=False)
            emoji = "✅" if status == 'win' else "❌"
            send_signal({
                "symbol": symbol, "side": side, "status": status,
                "exit_price": exit_price, "pnl": pnl
            })
            print(f"[ {now} ] {emoji} EXIT — {symbol} status={status}", flush=True)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
