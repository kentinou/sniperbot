import pandas as pd

# ----- Bougie Patterns -----
def is_marubozu(open_price, close_price, high, low, threshold=0.03):
    body = abs(close_price - open_price)
    candle_range = high - low
    if candle_range == 0:
        return False
    return (body / candle_range) > (1 - threshold)

def is_engulfing(prev_open, prev_close, curr_open, curr_close):
    return (
        (curr_open < curr_close and prev_open > prev_close and curr_open < prev_close and curr_close > prev_open) or
        (curr_open > curr_close and prev_open < prev_close and curr_open > prev_close and curr_close < prev_open)
    )

# ----- Tendance EMA -----
def get_trend(ema9, ema21):
    if ema9 > ema21:
        return "up"
    elif ema9 < ema21:
        return "down"
    else:
        return "neutral"

# ----- Score de Confiance -----
def calculate_confidence(rsi, ema9, ema21, volume_now, volume_ma,
                         ema9_h1, ema21_h1, ema9_1d, ema21_1d,
                         atr_ok, candle_pattern):
    confidence = 0

    if rsi < 30 or rsi > 70:
        confidence += 20

    if (ema9 > ema21) or (ema9 < ema21):
        confidence += 20

    if volume_now > volume_ma:
        confidence += 15

    if get_trend(ema9, ema21) == get_trend(ema9_h1, ema21_h1) and get_trend(ema9, ema21) != "neutral":
        confidence += 15

    if get_trend(ema9, ema21) == get_trend(ema9_1d, ema21_1d) and get_trend(ema9, ema21) != "neutral":
        confidence += 10

    if atr_ok:
        confidence += 10

    if candle_pattern:
        confidence += 10

    return round(min(confidence, 100), 1)

# ----- Analyse complète du signal -----
def analyse_signal(df_5m, df_15m, df_1h, df_1d):
    last_candle = df_5m.iloc[-1]
    prev_candle = df_5m.iloc[-2]

    rsi = last_candle['rsi']
    ema9 = last_candle['ema9']
    ema21 = last_candle['ema21']
    volume_now = last_candle['volume']
    volume_ma = df_5m['volume'].tail(20).mean()

    ema9_h1 = df_1h['ema9'].iloc[-1]
    ema21_h1 = df_1h['ema21'].iloc[-1]
    ema9_1d = df_1d['ema9'].iloc[-1]
    ema21_1d = df_1d['ema21'].iloc[-1]

    atr_ok = True  # TODO: ajouter une vraie vérification ATR

    candle_pattern = (
        is_marubozu(last_candle['open'], last_candle['close'], last_candle['high'], last_candle['low']) or
        is_engulfing(prev_candle['open'], prev_candle['close'], last_candle['open'], last_candle['close'])
    )

    confidence = calculate_confidence(
        rsi, ema9, ema21,
        volume_now, volume_ma,
        ema9_h1, ema21_h1,
        ema9_1d, ema21_1d,
        atr_ok, candle_pattern
    )

    signal = None
    if rsi < 30 and ema9 > ema21:
        signal = "LONG"
    elif rsi > 70 and ema9 < ema21:
        signal = "SHORT"

    return {
        "signal": signal,
        "confidence": confidence,
        "rsi": round(rsi, 2),
        "ema_trend": get_trend(ema9, ema21),
        "volume_now": round(volume_now),
        "volume_ma": round(volume_ma),
        "candle_pattern": "Yes" if candle_pattern else "No"
    }
