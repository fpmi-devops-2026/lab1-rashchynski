# Отчет по лабораторной работе №1
## Дисциплина: Непрерывное интегрирование и сборка программного обеспечения

**Студент:** Ращинский Назар Андреевич  
**Группа:** 11  

---

## Цель работы
Изучение современных технологий контейнеризации.

## Вариант
Группа 11 (выполнение всех 6 заданий).
---

## Задание 1. Основы управления контейнерами и образами Docker

### Ход выполнения работы

Для запуска трех контейнеров Nginx с различными тегами и пробросом портов на хост-систему использовались команды:

```Bash
docker run -d -p 8081:80 --name mynginxlast nginx:latest
docker run -d -p 8082:80 --name mynginxalpine nginx:alpine
docker run -d -p 8083:80 --name mynginx1-28 nginx:1.28
```

Просмотр активных контейнеров и скачанных образов выполнялся командами:
```Bash
docker ps
docker images
```
Просмотр списка запущенных контейнеров (docker ps):
```Bash
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                  NAMES
4c3c471bad25   nginx:alpine   "/docker-entrypoint.…"   2 minutes ago   Up 2 minutes   0.0.0.0:8082->80/tcp   mynginxalpine
9384177d4313   nginx:latest   "/docker-entrypoint.…"   2 minutes ago   Up 2 minutes   0.0.0.0:8081->80/tcp   mynginxlast
e70cfb92a1b0   nginx:1.28     "/docker-entrypoint.…"   2 minutes ago   Up 2 minutes   0.0.0.0:8083->80/tcp   mynginx1-28
```
Просмотр загруженных локально образов (docker images):
```Bash
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        latest    abe47724e466   2 days ago     188MB
nginx        alpine    62ff2089abf5   2 days ago     42.6MB
nginx        1.28      146adea4768b   2 weeks ago    188MB
ubuntu       latest    da6fc2be5478   3 weeks ago    78.1MB
```

Остановка и удаление контейнера mynginx1-28 выполнены командами: 

```Bash
docker stop mynginx1-28
docker rm mynginx1-28
```
```
mynginx1-28
mynginx1-28
```

Для подключения к запущенному контейнеру в интерактивном режиме с вызовом командной оболочки применялась команда: 
```Bash
docker exec -it mynginxlast sh.
```

```
/ # ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
/ # exit
```

Запуск отдельного временного контейнера Ubuntu в интерактивном режиме выполнен через:
```Bash
docker run -it --name test_ubuntu ubuntu bash
```

```
root@ce79a83011d6:/# whoami
root
root@ce79a83011d6:/# exit
exit
```

Для демонстрации монтирования томов в каталоге task1 был создан файл index.html.    
Контейнер mynginxalpine пересоздан с привязкой текущей рабочей директории к корню веб-сервера Nginx:
```Bash
docker stop mynginxalpine && docker rm mynginxalpine
docker run -d -p 8082:80 --name mynginxalpine -v $(pwd):/usr/share/nginx/html:ro nginx:alpine
```

Исходный код файла task1/index.html:
```HTML
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Лабораторная работа №1</title>
</head>
<body>
    <h1>Задание 1. Основы управления контейнерами и образами Docker</h1>
    <p>ФИО: Ращинский Назар Андреевич</p>
    <p>Группа: 11</p>
</body>
</html>
```

Результаты работы и тестирования      
Запрос к смонтированной странице через 
```curl http://localhost:8082```

возвращает сформированный HTML-документ:
```HTML
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Лабораторная работа №1</title>
</head>
<body>
    <h1>Задание 1. Основы управления контейнерами и образами Docker</h1>
    <p>ФИО: Ращинский Назар Андреевич</p>
    <p>Группа: 11</p>
</body>
</html>
```

---

## Задание 2. Создание и публикация собственного Docker-образа в Docker Hub

### Ход выполнения работы

Исходный код файла task2/index.html:
```HTML
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Лабораторная работа №1 — Задание 2</title>
</head>
<body>
    <h1>Задание 2. Сборка собственного Docker-образа</h1>
    <p>ФИО: Ращинский Назар Андреевич</p>
    <p>Группа: 11</p>
</body>
</html>
```

Исходный код файла task2/Dockerfile:
```Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Ход выполнения работы и консольный вывод:

Сборка собственного образа локально:
```Bash
$ docker build -t nrashchynski/lab1-custom-nginx:v1.0 .
```

Запуск и проверка работы контейнера из собранного образа:
```Bash
$ docker run -d -p 8084:80 --name mycustomnginx nrashchynski/lab1-custom-nginx:v1.0
$ curl http://localhost:8084
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Лабораторная работа №1 — Задание 2</title>
</head>
<body>
    <h1>Задание 2. Сборка собственного Docker-образа</h1>
    <p>ФИО: Ращинский Назар Андреевич</p>
    <p>Группа: 11</p>
</body>
</html>
```

Публикация образа в реестр Docker Hub:
```Bash
$ docker push nrashchynski/lab1-custom-nginx:v1.0
The push refers to repository [docker.io/nrashchynski/lab1-custom-nginx]
a9986cd6f37d: Mounted from library/nginx 
803b7c3361ce: Pushed 
44136fa355b3: Pushed 
4e9ebb12c87e: Mounted from library/nginx 
18eb23b7676d: Mounted from library/nginx 
218624bde535: Mounted from library/nginx 
3ef3eba6b71c: Mounted from library/nginx 
e24c840b9291: Mounted from library/nginx 
701fee9236d6: Mounted from library/nginx 
2f062a0d6c6f: Pushed 
7b9f6954712c: Mounted from library/nginx 
v1.0: digest: sha256:c8f5a97e64666d3feb6ba8141dde915ac6182a82dcf8fbc55d9a356d806d1b96 size: 856
EOF
```
---

## Задание 3. Контейнеризация простого веб-приложения (Python/Flask)

### Ход выполнения работы

Исходный код файла task3/app.py:
```python
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
```

Исходный код файла task3/requirements.txt:
```txt
Flask==3.0.3
```

Исходный код файла task3/Dockerfile:
```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV APP_TITLE="Лабораторная работа №1 — Задание 3 (Python/Flask)"

EXPOSE 5000

CMD ["python", "app.py"]
```

Ход выполнения работы и консольный вывод:
Сборка собственного образа Python/Flask:
```Bash
$ docker build -t nrashchynski/lab1-python-app:v1.0 .
```
```
[+] Building 20.5s (10/10) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [1/5] FROM docker.io/library/python:3.11-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY app.py .
 => naming to docker.io/nrashchynski/lab1-python-app:v1.0
 ```

Запуск контейнера с переопределением переменной окружения ENV (-e):
```Bash
$ docker run -d -p 5001:5000 --name myflaskapp -e APP_TITLE="Задание 3: Демонстрация ENV в Flask" nrashchynski/lab1-python-app:v1.0
```
```
d54a7021bf25ba3ad131fd3d15cffc276ba1d2562b8afd66fd006f757532a137
```

Проверка работы сервиса по порту 5001 (curl):
```Bash
$ curl http://localhost:5001
```
```Bash
<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Задание 3: Демонстрация ENV в Flask</title>
    </head>
    <body>
        <h1>Задание 3: Демонстрация ENV в Flask</h1>
        <p>ФИО: Ращинский Назар Андреевич</p>
        <p>Группа: 11</p>
        <p>Приложение: Python / Flask</p>
    </body>
    </html>
```

Публикация образа в реестре Docker Hub:
```Bash
$ docker push nrashchynski/lab1-python-app:v1.0
```
```
The push refers to repository [docker.io/nrashchynski/lab1-python-app]
e6c2e040f413: Already exists 
44136fa355b3: Already exists 
03f370686e3a: Layer already exists 
v1.0: digest: sha256:2fcc373e88310b6db36e7bd2aadcc0618b1d3feb8e40123ca2c65e8c2a12a65d size: 856
```

---

## Задание 4. Описание многоконтейнерных приложений с помощью Docker Compose

### Ход выполнения работы

Исходный код файла task4/.env:
```
APP_PORT=5000
NGINX_PORT=8080
APP_TITLE=Задание 4: Docker Compose (Flask + Nginx Reverse Proxy)
```

Исходный код файла task4/nginx.conf:
```
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;

        location / {
            proxy_pass http://app:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

Исходный код файла task4/docker-compose.yml:
```
services:
  app:
    image: nrashchynski/lab1-python-app:v1.0
    container_name: compose-flask-app
    environment:
      - APP_TITLE=${APP_TITLE}
    networks:
      - app-network

  proxy:
    image: nginx:latest
    container_name: compose-nginx-proxy
    ports:
      - "${NGINX_PORT}:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

```

Ход выполнения работы и консольный вывод:
Запуск сервисов в фоновом режиме:
```Bash
$ docker compose up -d
```
```
[+] up 3/3
 ✔ Network task4_app-network     Created
 ✔ Container compose-flask-app   Started
 ✔ Container compose-nginx-proxy Started
 ```

 Проверка статуса контейнеров:
 ```Bash
 $ docker compose ps
 ```
 ```
NAME                  IMAGE                               COMMAND                  SERVICE   CREATED          STATUS          PORTS
compose-flask-app     nrashchynski/lab1-python-app:v1.0   "python app.py"          app       About a minute   Up About a minute 5000/tcp
compose-nginx-proxy   nginx:latest                        "/docker-entrypoint.…"   proxy     About a minute   Up About a minute 0.0.0.0:8080->80/tcp
```

Проверка ответа reverse proxy:
```
$ curl http://localhost:8080
```
```
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Задание 4: Docker Compose (Flask + Nginx Reverse Proxy)</title>
</head>
<body>
    <h1>Задание 4: Docker Compose (Flask + Nginx Reverse Proxy)</h1>
    <p>ФИО: Ращинский Назар Андреевич</p>
    <p>Группа: 11</p>
    <p>Приложение: Python / Flask</p>
</body>
</html>
```

Просмотр объединенных логов:
```
$ docker compose logs
```
```
compose-flask-app    | 172.18.0.3 - - [23/Sep/2026 19:29:48] "GET / HTTP/1.1" 200 -
compose-nginx-proxy  | 192.168.65.1 - - [23/Sep/2026:19:29:48 +0000] "GET / HTTP/1.1" 200 457 "-" "curl/8.7.1"
```

Остановка и удаление инфраструктуры:
```
$ docker compose down
```
[+] down 3/3
 ✔ Container compose-nginx-proxy Removed                                                    0.1s
 ✔ Container compose-flask-app   Removed                                                    3.1s
 ✔ Network task4_app-network     Removed 
 ```






