def analyse_signal(df_1h, df_1m, symbol):
    try:
        # Conversion en float
        df_1m['open'] = df_1m['open'].astype(float)
        df_1m['close'] = df_1m['close'].astype(float)
        df_1m['low'] = df_1m['low'].astype(float)
        df_1m['high'] = df_1m['high'].astype(float)

        # Au moins 2 bougies vertes consécutives à la fin
        consecutive_greens = 0
        for i in range(len(df_1m) - 1, -1, -1):
            if df_1m['close'].iloc[i] > df_1m['open'].iloc[i]:
                consecutive_greens += 1
            else:
                break
        if consecutive_greens < 2:
            return None

# Nouvelle logique : Fibo basé sur 30 bougies mensuelles
        df_range = df_1m.tail(30)
        low_idx = df_range['low'].idxmin()
        high_idx = df_range['high'][low_idx:].idxmax() if low_idx < len(df_range) else df_range['high'].idxmax()
        min_price = df_range['low'].loc[low_idx]
        max_price = df_range['high'].loc[high_idx]


        # Calcul Fibonacci du haut vers le bas
        fib_0 = max_price
        fib_0236 = max_price - 0.236 * (max_price - min_price)
        fib_0382 = max_price - 0.382 * (max_price - min_price)
        fib_05 = max_price - 0.5 * (max_price - min_price)
        fib_0618 = max_price - 0.618 * (max_price - min_price)
        fib_07 = max_price - 0.7 * (max_price - min_price)
        fib_0786 = max_price - 0.786 * (max_price - min_price)
        fib_1 = min_price

        price = float(df_1h['close'].iloc[-1])
        prev_price = float(df_1h['close'].iloc[-2])

        # Signal approche 0.618 venant du haut (tolérance 3%)
        if prev_price > fib_0618 and fib_0618 <= price <= fib_0618 * 1.03:
            return f"""🟢 LONG {symbol}
💰 Entrée : {round(fib_0618, 8)} USDT
🎯 TP1 : {round(fib_05, 8)}
🎯 TP2 : {round(fib_0382, 8)}
🎯 TP Final : {round(fib_0, 8)}
🛡️ SL : {round(fib_1, 8)} (niveau 1.0 du Fibo)
❔ Approche du niveau 0.618 mensuel (retracement)"""

        # Signal approche 0.7 venant du haut (tolérance 3%)
        if prev_price > fib_07 and fib_07 <= price <= fib_07 * 1.03:
            return f"""🟢 LONG {symbol}
💰 Entrée : {round(fib_07, 8)} USDT
🎯 TP1 : {round(fib_05, 8)}
🎯 TP2 : {round(fib_0382, 8)}
🎯 TP Final : {round(fib_0, 8)}
🛡️ SL : {round(fib_1, 8)} (niveau 1.0 du Fibo)
❔ Approche du niveau 0.7 mensuel (retracement)"""

        return None
    except Exception:
        return None
