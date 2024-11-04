# Utiliser une image de base Python 3.11
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements dans l'image
COPY ./src/requirements.txt /app/requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY ./src /app/src

# WORKDIR /app/src

# Exposer le port sur lequel l'application s'exécute (par défaut, FastAPI utilise 8000)
EXPOSE 8001

# Démarrer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
