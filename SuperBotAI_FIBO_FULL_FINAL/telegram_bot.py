import requests

TOKEN = "8093249984:AAEysv-W_6NSF64tbeKjk8stqIKInBcX_7w"
CHAT_ID = "7290247547"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")