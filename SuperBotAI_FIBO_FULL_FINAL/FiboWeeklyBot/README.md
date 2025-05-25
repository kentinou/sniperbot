# FiboWeeklyBot

Ce bot détecte les signaux basés sur le niveau 0.618 de Fibonacci hebdomadaire avec entrée automatique, TP, SL, et notifications Telegram.

## Fonctionnement :
- Analyse les bougies 1W pour définir le Fibo.
- Analyse EMA sur 1H pour la tendance.
- Entrée sur le niveau 0.618, TP sur 0.5.
- SL basé sur ATR 15m.
- Suivi des positions toutes les minutes.
- Logs dans performance_log.csv.

## Démarrage
```bash
pip install -r requirements.txt
python run_bot.py
```
