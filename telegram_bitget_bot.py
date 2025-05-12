import os
from bitget.openapi.client import Client
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Variables depuis .env
API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Connexion à Bitget
bitget_client = Client(API_KEY, API_SECRET, API_PASSPHRASE, use_server_time=True)

async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        order = bitget_client.mix_place_order(
            symbol='BTCUSDT',
            marginCoin='USDT',
            side='open_long',
            orderType='market',
            size='0.001',
            price='',  # vide pour market
            tradeSide='long',
            productType='usdt-futures'
        )
        await update.message.reply_text("✅ Ordre d'achat market BTCUSDT passé avec succès.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur lors de l'achat : {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("buy", buy_command))
    print("🤖 Bot en ligne. Envoie /buy pour tester.")
    app.run_polling()
