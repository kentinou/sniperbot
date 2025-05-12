import os
import imaplib
import email
from email.header import decode_header
import time
from bitget.spot.trade import Trade
from dotenv import load_dotenv

# Load credentials
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_IMAP_SERVER = os.getenv("EMAIL_IMAP_SERVER")

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
PASSPHRASE = os.getenv("BITGET_PASSPHRASE")

# === CONFIGURE BOT ===
SYMBOL = "BTCUSDT_UMCBL"
ORDER_SIZE = 0.001
LEVERAGE = 5

# === Connect to Bitget ===
trade = Trade(API_KEY, API_SECRET, PASSPHRASE)

def place_order(side: str):
    try:
        result = trade.place_order(
            symbol=SYMBOL,
            marginCoin="USDT",
            side=side,
            orderType="market",
            size=str(ORDER_SIZE),
            price="",
            timeInForceValue="normal"
        )
        print(f"✅ Order placed: {side.upper()} | {result}")
    except Exception as e:
        print(f"❌ Error placing order: {e}")

def process_email(subject, body):
    if "long" in subject.lower() or "long" in body.lower():
        place_order("open_long")
    elif "short" in subject.lower() or "short" in body.lower():
        place_order("open_short")
    else:
        print("📭 No trading signal found.")

def check_email():
    try:
        mail = imaplib.IMAP4_SSL(EMAIL_IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        for email_id in email_ids:
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    subject = subject.decode() if isinstance(subject, bytes) else subject

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    print(f"📨 New email: {subject}")
                    process_email(subject, body)

        mail.logout()
    except Exception as e:
        print(f"❌ Email check error: {e}")

# === Main loop ===
print("📡 Email to Bitget bot started...")
while True:
    check_email()
    time.sleep(10)
