
import pandas as pd
from core.risk_manager import calculate_atr

def is_bullish_trend(df_1h):
    ema20 = df_1h['close'].ewm(span=20).mean()
    ema50 = df_1h['close'].ewm(span=50).mean()
    return ema20.iloc[-1] > ema50.iloc[-1]

def is_bearish_trend(df_1h):
    ema20 = df_1h['close'].ewm(span=20).mean()
    ema50 = df_1h['close'].ewm(span=50).mean()
    return ema20.iloc[-1] < ema50.iloc[-1]

def analyse_signal(df_1w, df_1h, df_15m):
    high = df_1w['high'].iloc[-1]
    low = df_1w['low'].iloc[-1]
    fib_0618 = low + 0.618 * (high - low)
    fib_0500 = low + 0.500 * (high - low)
    close = df_15m['close'].iloc[-1]

    atr = calculate_atr(df_15m)

    if abs(close - fib_0618) <= atr * 0.1:
        if is_bullish_trend(df_1h):
            return {
                "signal": "LONG",
                "entry": close,
                "tp": fib_0500,
                "sl": close - atr,
                "confidence": 90,
                "reason": "Fibo 0.618 + Tendance H1 haussière"
            }
        elif is_bearish_trend(df_1h):
            return {
                "signal": "SHORT",
                "entry": close,
                "tp": fib_0500,
                "sl": close + atr,
                "confidence": 90,
                "reason": "Fibo 0.618 + Tendance H1 baissière"
            }
    return {"signal": None}
