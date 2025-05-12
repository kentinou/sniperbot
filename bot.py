import os
import asyncio
import uvicorn
from fastapi import FastAPI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from bitget_sdk.openapi.client import Client

load_dotenv()

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bitget_client = Client(API_KEY, API_SECRET, API_PASSPHRASE, use_server_time=True)
bot_active = {"status": False}
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "SuperBossSniperBot opérationnel"}

# Commande /buy
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🚀 Envoi d’un ordre LONG 0.001 BTCUSDT (futures)...")
        result = bitget_client.mix_place_order(
            symbol='BTCUSDT',
            marginCoin='USDT',
            size='0.001',
            side='open_long',
            orderType='market',
            price='',
            tradeSide='long',
            productType='usdt-futures'
        )
        await update.message.reply_text(f"✅ Réponse Bitget : {result}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur API Bitget : {str(e)}")

# Démarrage Telegram (ApplicationBuilder v22+)
async def run_bot():
    app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_telegram.add_handler(CommandHandler("buy", buy))
    await app_telegram.run_polling()

# Lancement Render
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_bot())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("bot:app", host="0.0.0.0", port=port)
