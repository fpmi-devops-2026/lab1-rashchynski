import os
from flask import Flask

app = Flask(__name__)

APP_TITLE = os.getenv("APP_TITLE", "Лабораторная работа №1 — Задание 3")

@app.route("/")
def hello():
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>{APP_TITLE}</title>
    </head>
    <body>
        <h1>{APP_TITLE}</h1>
        <p>ФИО: Ращинский Назар Андреевич</p>
        <p>Группа: 11</p>
        <p>Приложение: Python / Flask</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)