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
        result = open_position()
        await update.message.reply_text(f"✅ Ordre BUY exécuté : {result}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur lors de l'achat : {str(e)}")

async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_active["status"] = True
    await update.message.reply_text("🤖 Bot activé. Scalping en cours...")
    await scalping_loop(update)

async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_active["status"] = False
    await update.message.reply_text("🛑 Bot arrêté.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = "actif" if bot_active["status"] else "inactif"
    await update.message.reply_text(f"📊 Le bot est actuellement : {status}")

def open_position():
    account = bitget_client.mix_get_account('BTCUSDT', 'usdt')
    balance = float(account['data']['available'])
    amount = round(balance * 0.02, 3)
    result = bitget_client.mix_place_order(
        symbol='BTCUSDT',
        marginCoin='USDT',
        size=str(amount),
        side='open_long',
        orderType='market',
        price='',
        tradeSide='long',
        productType='usdt-futures'
    )
    return result

def close_positions():
    bitget_client.mix_place_order(
        symbol='BTCUSDT',
        marginCoin='USDT',
        size='0.001',
        side='close_long',
        orderType='market',
        price='',
        tradeSide='long',
        productType='usdt-futures'
    )

async def scalping_loop(update: Update = None):
    while bot_active["status"]:
        try:
            res = open_position()
            if update:
                await update.message.reply_text("📈 Position ouverte.")
            await asyncio.sleep(10)
            close_positions()
            if update:
                await update.message.reply_text("💰 Position fermée (scalp).")
            await asyncio.sleep(5)
        except Exception as e:
            if update:
                await update.message.reply_text(f"⚠️ Erreur : {str(e)}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("start", start_bot))
    app.add_handler(CommandHandler("stop", stop_bot))
    app.add_handler(CommandHandler("status", status))
    print("🤖 SuperBossSniperBot en ligne.")
    app.run_polling()
