# Utiliser l'image correcte de Python
FROM python:3.13

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY ./requirements.txt /app/requirements.txt

# Installer les dépendances de requirements.txt
RUN pip install -r requirements.txt

# Copier tout le contenu de l'application dans le conteneur
COPY ./* /app/

# Exposer le port (optionnel, mais utile pour Docker)
EXPOSE 80

# Commande pour démarrer l'application FastAPI avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
