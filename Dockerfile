FROM python:3.12-slim
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py makemigrations verleih
RUN python manage.py migrate
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
