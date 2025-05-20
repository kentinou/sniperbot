import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "8093249984:AAEysv-W_6NSF64tbeKjk8stqIKInBcX_7w"
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "7290247547"

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Erreur Telegram: {response.status_code} – {response.text}")
    except Exception as e:
        print(f"Exception lors de l'envoi Telegram : {e}")
