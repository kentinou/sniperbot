import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from bitget_sdk.openapi.client import Client

load_dotenv()

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bitget_client = Client(API_KEY, API_SECRET, API_PASSPHRASE, use_server_time=True)
bot_active = {"status": False}

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        order = bitget_client.mix_place_order(
            symbol='BTCUSDT',
            marginCoin='USDT',
            size='0.001',
            side='open_long',
            orderType='market',
            price='',
            tradeSide='long',
            productType='usdt-futures'
        )
        await update.message.reply_text("✅ Ordre d'achat market BTCUSDT exécuté.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur lors de l'achat : {str(e)}")

async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_active["status"] = True
    await update.message.reply_text("🤖 Bot activé. Trading automatique en cours...")

async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_active["status"] = False
    await update.message.reply_text("🛑 Bot arrêté.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = "actif" if bot_active["status"] else "inactif"
    await update.message.reply_text(f"📊 Le bot est actuellement : {status}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("start", start_bot))
    app.add_handler(CommandHandler("stop", stop_bot))
    app.add_handler(CommandHandler("status", status))
    print("🤖 SuperBossSniperBot en ligne.")
    app.run_polling()
