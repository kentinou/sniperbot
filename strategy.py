import os
import pandas as pd
from config import SYMBOLS_TO_SCAN as ALL_SYMBOLS
from binance_api import get_ohlcv
from utils import calculate_rsi, calculate_atr
from telebot import send_signal
from datetime import datetime
from zoneinfo import ZoneInfo

# Définir le chemin absolu du CSV à la racine du repo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "signaux.csv")

# Exclusions et seuils RSI ajustés pour plus de signaux
EXCLUDE = {"LEVERUSDT", "BMTUSDT", "SPKUSDT", "OBOLUSDT", "BTCDOMUSDT", "BRUSDT"}
THRESHOLD_LONG = 20    # RSI < 20 pour signal long
THRESHOLD_SHORT = 80   # RSI > 80 pour signal short

# Timeframes à scanner
TIMEFRAMES = ["1d", "4h", "1w"]
brussels_tz = ZoneInfo("Europe/Brussels")

# Paramètres pour détection de divergence classique assouplis
PIVOT_LOOKBACK     = 100   # on regarde les 100 dernières barres
LEFT, RIGHT        = 3, 3   # fenêtre pour pivots
MIN_BAR_DISTANCE   = 5     # écart min réduit entre pivots
MIN_PRICE_DIFF_PCT = 0.01  # 1% de différence de prix minimale
MIN_RSI_DIFF       = 3.0   # 3 points de RSI minimum


def find_pivots(series: pd.Series, left: int = LEFT, right: int = RIGHT, kind: str = "high") -> list:
    """Retourne les indices de pivot haut ou bas dans les PIVOT_LOOKBACK dernières barres."""
    pivots = []
    data = series.iloc[-PIVOT_LOOKBACK:]
    for idx in range(left, len(data) - right):
        window = data.iloc[idx-left : idx+right+1]
        val = data.iloc[idx]
        if (kind == "high" and val == window.max()) or (kind == "low" and val == window.min()):
            pivots.append(data.index[idx])
    return pivots


def run_scan():
    # Lecture du CSV existant
    try:
        df_sig = pd.read_csv(CSV_FILE)
        open_symbols = set(df_sig[df_sig["status"] == "open"]["symbol"])
    except FileNotFoundError:
        open_symbols = set()

    symbols = [s for s in ALL_SYMBOLS if s not in EXCLUDE and s not in open_symbols]
    timeframe_labels = "/".join(tf.upper() for tf in TIMEFRAMES)
    print(f"[{datetime.now(brussels_tz)}] 🔍 Scan de {len(symbols)} symbols sur {timeframe_labels}", flush=True)

    for symbol in symbols:
        for tf in TIMEFRAMES:
            try:
                # Récupérer OHLCV suffisant
                df = get_ohlcv(symbol, interval=tf, limit=PIVOT_LOOKBACK + RIGHT)
                rsi = calculate_rsi(df["close"], period=14)
                if len(rsi) < PIVOT_LOOKBACK:
                    continue

                # Indices de pivots
                idx_high = find_pivots(df["high"], kind="high")
                idx_low  = find_pivots(df["low"],  kind="low")
                # Debug: afficher le nombre de pivots détectés
                print(f"{symbol} [{tf}] -> pivots_high: {len(idx_high)}, pivots_low: {len(idx_low)}", flush=True)

                # Divergence baissière
                bearish_div = False
                if len(idx_high) >= 2:
                    t1, t2 = idx_high[-2], idx_high[-1]
                    if (df.index.get_loc(t2) - df.index.get_loc(t1)) >= MIN_BAR_DISTANCE:
                        price1, price2 = df.at[t1, "high"], df.at[t2, "high"]
                        rsi1, rsi2     = rsi.loc[t1],               rsi.loc[t2]
                        print(f"  High pivots at {t1}/{t2} prices {price1:.4f}/{price2:.4f} RSI {rsi1:.2f}/{rsi2:.2f}", flush=True)
                        bearish_div = (price2 > price1 * (1 + MIN_PRICE_DIFF_PCT)
                                       and rsi2 < rsi1 - MIN_RSI_DIFF)
                        print(f"  bearish_div={bearish_div}", flush=True)

                # Divergence haussière
                bullish_div = False
                if len(idx_low) >= 2:
                    u1, u2 = idx_low[-2], idx_low[-1]
                    if (df.index.get_loc(u2) - df.index.get_loc(u1)) >= MIN_BAR_DISTANCE:
                        low1, low2    = df.at[u1, "low"], df.at[u2, "low"]
                        rsi_u1, rsi_u2 = rsi.loc[u1],        rsi.loc[u2]
                        print(f"  Low pivots at {u1}/{u2} lows {low1:.4f}/{low2:.4f} RSI {rsi_u1:.2f}/{rsi_u2:.2f}", flush=True)
                        bullish_div = (low2 < low1 * (1 - MIN_PRICE_DIFF_PCT)
                                       and rsi_u2 > rsi_u1 + MIN_RSI_DIFF)
                        print(f"  bullish_div={bullish_div}", flush=True)

                # RSI actuel et décision
                rsi_now = rsi.iloc[-1]
                print(f"  Current RSI={rsi_now:.2f}", flush=True)
                if rsi_now > THRESHOLD_SHORT and bearish_div:
                    side = "sell"
                elif rsi_now < THRESHOLD_LONG and bullish_div:
                    side = "buy"
                else:
                    print(f"  Pas de signal pour {symbol} [{tf}]", flush=True)
                    continue

                # Calcul ATR, TP/SL
                entry = df["close"].iloc[-1]
                atr   = calculate_atr(df["high"], df["low"], df["close"], period=14).iloc[-1]
                tp    = entry + atr if side == "buy" else entry - atr
                sl    = entry - atr if side == "buy" else entry + atr

                # Préparer et écrire le signal dans le CSV
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
                df_new = pd.DataFrame([sig])
                if not os.path.exists(CSV_FILE):
                    df_new.to_csv(CSV_FILE, index=False)
                else:
                    df_new.to_csv(CSV_FILE, mode='a', header=False, index=False)

                # Envoi Telegram et log
                send_signal(sig)
                emoji = "🟢" if side == "buy" else "🔴"
                print(f"[{datetime.now(brussels_tz)}] {emoji} SIGNAL {tf.upper()} — {symbol} | Entry={entry:.6f} | TP={tp:.6f} | SL={sl:.6f}", flush=True)

            except Exception as e:
                print(f"[{datetime.now(brussels_tz)}] ❌ Erreur {symbol} ({tf}) : {e}", flush=True)

if __name__ == "__main__":
    run_scan()
