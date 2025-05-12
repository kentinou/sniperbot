# SuperBossSniperBot

Bot Telegram de trading automatique sur Bitget. Déployable sur Render.

## Déploiement Render

1. Connecte ton GitHub contenant ce projet à Render.
2. Crée un service Web Python.
3. Start Command : `python bot.py`
4. Ajoute les variables d'environnement suivantes :

- `BITGET_API_KEY`
- `BITGET_API_SECRET`
- `BITGET_PASSPHRASE`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

5. Lance `/start` depuis Telegram pour activer la stratégie.
