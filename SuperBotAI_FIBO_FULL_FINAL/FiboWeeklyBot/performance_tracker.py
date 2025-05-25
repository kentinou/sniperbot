
import pandas as pd
from datetime import datetime

LOG_FILE = "performance_log.csv"

def log_trade(symbol, direction, entry, tp, sl, result, pnl):
    time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    row = pd.DataFrame([[time, symbol, direction, entry, tp, sl, result, pnl]],
        columns=["time", "symbol", "direction", "entry", "tp", "sl", "result", "pnl"])
    try:
        old = pd.read_csv(LOG_FILE)
        row = pd.concat([old, row])
    except:
        pass
    row.to_csv(LOG_FILE, index=False)
