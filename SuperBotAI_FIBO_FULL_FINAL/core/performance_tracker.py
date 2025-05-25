
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

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

def plot_equity():
    df = pd.read_csv(LOG_FILE)
    df["cumsum"] = df["pnl"].cumsum()
    plt.figure(figsize=(10, 4))
    plt.plot(df["time"], df["cumsum"], label="Capital")
    plt.xticks(rotation=45)
    plt.title("Courbe des performances")
    plt.tight_layout()
    plt.savefig("equity_curve.png")
