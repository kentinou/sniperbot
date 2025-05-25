
import time
from core.data_utils import get_symbols, get_klines
from core.signal_generator_fibo_week import analyse_signal
from core.performance_tracker import log_trade
from telegram_bot import send_telegram
from datetime import datetime, timezone

def run():
    symbols = get_symbols()
    for sym in symbols:
        try:
            df_15m = get_klines(sym, interval="15m", limit=100)
            df_1h = get_klines(sym, interval="1h", limit=100)
            df_1w = get_klines(sym, interval="1w", limit=2)

            if df_15m.empty or df_1h.empty or df_1w.empty:
                continue

            result = analyse_signal(df_1w, df_1h, df_15m)

            if result["signal"]:
                now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
                emoji = "🟢" if result["signal"] == "LONG" else "🔴"

                msg = (
                    f"{emoji} *Signal {result['signal']}* sur {sym}\n"
                    f"🕒 {now} (Fibo 0.618 hebdo)\n"
                    f"💰 Entrée : {result['entry']:.4f}\n"
                    f"🎯 TP : {result['tp']:.4f}\n"
                    f"🛡️ SL : {result['sl']:.4f}\n"
                    f"🧠 Confiance : {result['confidence']}%\n"
                    f"📌 Raisons : {result['reason']}"
                )
                send_telegram(msg)
                log_trade(sym, result["signal"], result["entry"], result["tp"], result["sl"], "pending", 0)

        except Exception as e:
            print(f"Erreur avec {sym}: {e}")

if __name__ == "__main__":
    while True:
        run()
        print("✅ Pause 5 min")
        time.sleep(300)
