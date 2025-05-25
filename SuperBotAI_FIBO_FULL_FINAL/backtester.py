
from core.data_utils import get_klines
from core.signal_generator_pro import analyse_signal_pro
from core.performance_tracker import log_trade, plot_equity

def backtest(symbol):
    df = get_klines(symbol, interval="15m", limit=500)
    if df.empty:
        return
    result = analyse_signal_pro(df)
    if result["signal"]:
        entry = df["close"].iloc[-1]
        tp = entry * (1.03 if result["signal"] == "LONG" else 0.97)
        sl = entry * (0.99 if result["signal"] == "LONG" else 1.01)
        result_type = "win" if (result["signal"] == "LONG" and df["high"].iloc[-1] >= tp) else "loss"
        pnl = tp - entry if result_type == "win" else sl - entry
        log_trade(symbol, result["signal"], entry, tp, sl, result_type, pnl)

if __name__ == "__main__":
    for symbol in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]:
        backtest(symbol)
    plot_equity()
