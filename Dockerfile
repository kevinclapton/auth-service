FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

EXPOSE 8000

# Запуск: сначала ждём БД и создаём таблицы, потом запускаем Uvicorn
CMD ["sh", "-c", "python app/wait_for_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]