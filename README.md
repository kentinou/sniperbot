# TrendlinePullbackScanner

Bot de détection de cassures de trendlines hebdomadaires avec confirmation pullback en M30 sur toutes les cryptos Binance Futures USDT.

## Installation (Render)

1. Créer un service web sur Render en Python 3.10+
2. Ajouter les fichiers suivants :
   - `TrendlinePullbackScanner.py`
   - `config.json` (remplir TOKEN Telegram + Chat ID)
3. Ajouter un fichier `requirements.txt` :

```
ccxt
requests
pandas
scipy
```

4. Commande de démarrage :

```
python TrendlinePullbackScanner.py
```

## Fonctionnement

- Scanne toutes les cryptos Binance Futures USDT chaque heure
- Trace une trendline baissière sur les plus hauts en 1W
- Si cassure + pullback confirmé en M30 : signal Telegram
