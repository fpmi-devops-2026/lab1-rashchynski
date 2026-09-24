FROM python:3.11-slim

RUN useradd -m -u 1000 app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN chown -R app:app /app

USER app

ENV APP_TITLE="Лабораторная работа №1 — Задание 3 (Python/Flask)"

EXPOSE 5000

CMD ["python", "app.py"]