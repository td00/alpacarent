# Verwende ein offizielles Python-Image als Basis
FROM python:3.12-slim

# Arbeitsverzeichnis im Container erstellen
WORKDIR /app

# Abhängigkeiten installieren (Git, für das Klonen des Repos, falls nicht vorhanden)
RUN apt-get update && apt-get install -y git

# Das gesamte Repository in den Container kopieren
COPY . /app/

# Installiere Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Um sicherzustellen, dass die statischen Dateien gesammelt werden
RUN python manage.py makemigrations verleih
RUN python manage.py migrate

# Exponiere den Port 8000
EXPOSE 8000

# Setze Umgebungsvariablen für Django
ENV DJANGO_SETTINGS_MODULE=verleih.settings
ENV PYTHONUNBUFFERED=1

# Starte den Django-Server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
