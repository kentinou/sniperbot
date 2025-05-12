# Email-to-Bitget Trading Bot 📬 → 📈

Ce bot lit les e-mails envoyés par TradingView à `kennybybi@gmail.com` et ouvre automatiquement des ordres sur Bitget.

## 🔧 Configuration

1. **Créer un mot de passe d'application Gmail**
   - Allez sur [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Choisissez "Mail" + "Autre" → `bitget-bot`
   - Copiez le mot de passe généré et collez-le dans `.env`

2. **Cloner le projet et configurer le `.env`**
   ```bash
   git clone https://github.com/toncompte/email-bitget-bot.git
   cd email-bitget-bot
   cp .env.example .env
   # Remplir les vraies valeurs dans .env
   ```

3. **Déployer sur Render**
   - Nouveau service → Background Worker
   - Dépôt GitHub : `email-bitget-bot`
   - Commande de démarrage : `python email_to_bitget_bot.py`
   - Variables d’environnement : copier-coller `.env`

## ✅ Triggers reconnus

- Sujet ou contenu de mail contenant **"long"** → ouvre un `open_long`
- Sujet ou contenu de mail contenant **"short"** → ouvre un `open_short`

## 🛠️ Dépendances
- Python 3.9+
- `pip install python-dotenv bitget`
