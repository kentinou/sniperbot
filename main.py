import time
from strategy import run_scan
from datetime import datetime
from zoneinfo import ZoneInfo

tz = ZoneInfo("Europe/Brussels")

if __name__ == "__main__":
    print(f"[ {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')} ] Bot démarré.", flush=True)
    while True:
        try:
            run_scan()
        except Exception as e:
            print(f"[ {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')} ] Erreur dans run_scan: {e}", flush=True)
        time.sleep(120)
