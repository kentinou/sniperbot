import requests

TOKEN = '8093249984:AAEysv-W_6NSF64tbeKjk8stqIKInBcX_7w'
CHAT_ID = '7290247547'

def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Erreur Telegram:", e)