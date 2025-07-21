import pandas as pd
from config import SYMBOLS_TO_SCAN as ALL_SYMBOLS
from binance_api import get_ohlcv
from utils import calculate_rsi, calculate_atr, save_signal
from telebot import send_signal
from datetime import datetime
from zoneinfo import ZoneInfo

# Liste des symbols à exclure et seuils de RSI pour divergence
EXCLUDE = {"LEVERUSDT", "BMTUSDT", "SPKUSDT", "OBOLUSDT", "BTCDOMUSDT", "BRUSDT"}
THRESHOLD_LONG  = 20     # RSI < 20 pour signal long
THRESHOLD_SHORT = 90     # RSI > 90 pour signal short

# Timeframes : 1 jour, 4 heures et 1 semaine
TIMEFRAMES = ["1d", "4h", "1w"]

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

    timeframe_labels = "/".join(tf.upper() for tf in TIMEFRAMES)
    print(f"[{datetime.now(brussels_tz)}] 🔍 Scan fusionné de {len(symbols)} symboles sur {timeframe_labels}", flush=True)

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
                # Short si RSI > THRESHOLD_SHORT avec divergence baissière
                if rsi_0 > THRESHOLD_SHORT and rsi_1 > rsi_0:
                    print(f"⚠️ CANDIDAT SHORT {tf.upper()} — {symbol} (RSI > {THRESHOLD_SHORT} avec divergence)", flush=True)
                    side = "sell"
                # Long si RSI < THRESHOLD_LONG avec divergence haussière
                elif rsi_0 < THRESHOLD_LONG and rsi_1 < rsi_0:
                    print(f"⚠️ CANDIDAT LONG {tf.upper()} — {symbol} (RSI < {THRESHOLD_LONG} avec divergence)", flush=True)
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
                print(f"[{datetime.now(brussels_tz)}] {emoji} SIGNAL {tf.upper()} — {symbol} | Entry={entry:.6f} | TP={tp:.6f} | SL={sl:.6f}", flush=True)

                break  # Arrêter après 1 signal par symbole

            except Exception as e:
                print(f"[{datetime.now(brussels_tz)}] ❌ Erreur {symbol} ({tf.upper()}) : {e}", flush=True)

if __name__ == "__main__":
    run_scan()
