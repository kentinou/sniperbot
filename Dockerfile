# Étape 1 : on part d'une image Python légère
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code
COPY . .

# Commande de démarrage : lance main.py et monitor.py en parallèle
CMD ["sh", "-c", "python main.py & python monitor.py"]
