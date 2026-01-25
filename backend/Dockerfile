# Image de base Python
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour MySQL
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du backend
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Commande par défaut (sera overridée par docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
