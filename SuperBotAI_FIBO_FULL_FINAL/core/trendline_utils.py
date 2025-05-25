import numpy as np

def detect_trendline_break(df):
    try:
        highs = df['high'].values
        closes = df['close'].values
        times = np.arange(len(highs))

        # Trouver les 3 plus hauts locaux pour tracer une tendance
        tops = []
        for i in range(1, len(highs)-1):
            if highs[i] > highs[i-1] and highs[i] > highs[i+1]:
                tops.append((i, highs[i]))
            if len(tops) >= 3:
                break

        if len(tops) < 3:
            return False  # Pas assez de points de contact

        # Prendre les 2 premiers tops pour une droite (x0, y0) -> (x1, y1)
        x0, y0 = tops[0]
        x1, y1 = tops[1]
        if x1 == x0:
            return False

        # Équation de la droite : y = ax + b
        a = (y1 - y0) / (x1 - x0)
        b = y0 - a * x0

        # Vérifier si le dernier cours (close) casse la ligne
        x_last = times[-1]
        trend_y = a * x_last + b
        price_now = closes[-1]

        return price_now > trend_y  # cassure par le haut
    except Exception as e:
        print(f"[Trendline Detection Error] {e}")
        return False