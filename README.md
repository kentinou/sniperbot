# MegaTrendlineScanner

Bot de trading qui scanne toutes les cryptos Binance Futures pour détecter les cassures de trendlines baissières formées sur 100 bougies mensuelles (1M). Confirmation par pullback en M30 et volumes explosifs.

## Fonctionnement

- Détection de trendlines sur 1M (100 bougies)
- Pullback validé sur M30 avec pic de volume
- Concordance vérifiée avec 1W, 1D, H4, H1
- Signal envoyé uniquement si toutes les conditions sont remplies

## Installation

```bash
pip install -r requirements.txt
python MegaTrendlineScanner.py
```
