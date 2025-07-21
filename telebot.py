import requests
from datetime import datetime
from zoneinfo import ZoneInfo

BOT_TOKEN = "8093249984:AAEysv-W_6NSF64tbeKjk8stqIKInBcX_7w"
CHAT_ID = "7290247547"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_signal(signal: dict):
    tz = ZoneInfo("Europe/Brussels")
    now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    symbol = signal['symbol']
    side = signal['side'].lower()
    if signal.get('status') == 'open':
        # Emoji for long/buy and short/sell
        entry_emoji = "🟢" if side == "buy" else "🔴"
        # Timeframe (H4, 1D, etc.)
        tf = signal.get('timeframe', '').upper()
        # Build message with timeframe
        text = (
            f"{entry_emoji} <b>{symbol}</b> <i>[{tf}]</i>\n"
            f"📥 <b>Entry:</b> <code>{signal['entry']:.6f}</code>\n"
            f"🎯 <b>TP:</b>    <code>{signal['tp']:.6f}</code>\n"
            f"❌ <b>SL:</b>    <code>{signal['sl']:.6f}</code>\n"
            f"<i>{now}</i>"
        )
    else:
        # Emoji for win or loss on exit
        emoji = "✅" if signal['status'] == 'win' else "❌"
        text = (
            f"{emoji} <b>{symbol} ({signal['side'].upper()}) — EXIT</b>\n"
            f"💵 <b>Exit:</b>    <code>{signal['exit_price']:.6f}</code>\n"
            f"📈 <b>P&L:</b>     <code>{signal['pnl']:.2%}</code>\n"
            f"<i>{now}</i>"
        )
    # Send to Telegram
    requests.get(
        f"{BASE_URL}/sendMessage",
        params={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    )
