import pandas as pd
from config import SYMBOLS_TO_SCAN as ALL_SYMBOLS
from binance_api import get_ohlcv
from utils import calculate_rsi, calculate_atr, save_signal
from telebot import send_signal
from datetime import datetime
from zoneinfo import ZoneInfo

EXCLUDE = {"LEVERUSDT", "BMTUSDT", "SPKUSDT", "OBOLUSDT"}
THRESHOLD_LONG  = 20
THRESHOLD_SHORT = 90
TIMEFRAMES = ["1d", "4h"]

brussels_tz = ZoneInfo("Europe/Brussels")

def run_scan():
    try:
        df_sig = pd.read_csv("signaux.csv")
        open_symbols = set(df_sig[df_sig["status"] == "open"]["symbol"])
    except FileNotFoundError:
        open_symbols = set()

    symbols = [
        s for s in ALL_SYMBOLS
        if s not in EXCLUDE and s not in open_symbols
    ]

    print(f"[{datetime.now(brussels_tz)}] 🔍 Scan fusionné de {len(symbols)} symboles sur 1D + H4", flush=True)

    for symbol in symbols:
        for tf in TIMEFRAMES:
            try:
                df = get_ohlcv(symbol, interval=tf, limit=100)
                rsi_series = calculate_rsi(df["close"], period=14)
                if len(rsi_series) < 3:
                    continue

                rsi_2 = rsi_series.iloc[-3]
                rsi_1 = rsi_series.iloc[-2]
                rsi_0 = rsi_series.iloc[-1]

                print(f"[{datetime.now(brussels_tz)}] {symbol} {tf.upper()} — RSI-2: {rsi_2:.2f}, RSI-1: {rsi_1:.2f}, RSI-0: {rsi_0:.2f}", flush=True)

                side = None
                if rsi_0 > THRESHOLD_SHORT and rsi_1 > rsi_0:
                    print(f"⚠️ CANDIDAT SHORT {tf.upper()} — {symbol} (RSI > 90 avec divergence)", flush=True)
                    side = "sell"
                elif rsi_0 < THRESHOLD_LONG and rsi_1 < rsi_0:
                    print(f"⚠️ CANDIDAT LONG {tf.upper()} — {symbol} (RSI < 20 avec divergence)", flush=True)
                    side = "buy"

                if not side:
                    continue

                entry = df["close"].iloc[-1]
                atr = calculate_atr(df["high"], df["low"], df["close"], period=14).iloc[-1]
                tp = entry + atr if side == "buy" else entry - atr
                sl = entry - atr if side == "buy" else entry + atr

                sig = {
                    "timestamp":  datetime.now(brussels_tz),
                    "symbol":     symbol,
                    "side":       side,
                    "entry":      entry,
                    "tp":         tp,
                    "sl":         sl,
                    "status":     "open",
                    "exit_price": "",
                    "pnl":        "",
                    "timeframe":  tf
                }
                save_signal(sig)
                send_signal(sig)
                emoji = "🟢" if side == "buy" else "🔴"
                print(f"[{datetime.now(brussels_tz)}] {emoji} {symbol} ({tf.upper()}) Entry={entry:.6f} TP={tp:.6f} SL={sl:.6f}", flush=True)

                # Stop après premier signal (priorité daily)
                break

            except Exception as e:
                print(f"[{datetime.now(brussels_tz)}] ❌ Erreur {symbol} ({tf.upper()}) : {e}", flush=True)

if __name__ == "__main__":
    run_scan()
