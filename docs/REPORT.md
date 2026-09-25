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

Исходный код файла task3/Dockerfile с поддержкой безопасности (non-root пользователь app):
```Dockerfile
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
```

Ход выполнения работы и консольный вывод:

Сборка собственного образа Python/Flask:
```Bash
$ docker build -t nrashchynski/lab1-python-app:v1.1 .
```
```
[+] Building 9.1s (12/12) FINISHED
 => [1/7] FROM docker.io/library/python:3.11-slim
 => [2/7] RUN useradd -m -u 1000 app
 => [3/7] WORKDIR /app
 => [4/7] COPY requirements.txt .
 => [5/7] RUN pip install --no-cache-dir -r requirements.txt
 => [6/7] COPY app.py .
 => [7/7] RUN chown -R app:app /app
 => naming to docker.io/nrashchynski/lab1-python-app:v1.1
 ```

Запуск контейнера с переопределением переменной окружения ENV (-e):
```Bash
$ docker run -d -p 5001:5000 --name myflaskapp -e APP_TITLE="Задание 3: Демонстрация ENV в Flask" nrashchynski/lab1-python-app:v1.1
```
```
d54a7021bf25ba3ad131fd3d15cffc276ba1d2562b8afd66fd006f757532a137
```

```
$ docker exec myflaskapp_v11 whoami
app
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

Анализ размера собранных образов:
```
$ docker image ls nrashchynski/lab1-python-app
```
```
IMAGE                               TAG     ID             DISK USAGE   CONTENT SIZE
nrashchynski/lab1-python-app        v1.0    2fcc373e8831   237MB        51.6MB
nrashchynski/lab1-python-app        v1.1    d79bf78670db   237MB        51.6MB
```

Публикация образа v1.1 в реестре Docker Hub:
```Bash
$ docker push nrashchynski/lab1-python-app:v1.1
```
```
The push refers to repository [docker.io/nrashchynski/lab1-python-app]
03f370686e3a: Layer already exists 
bd36565c0fde: Layer already exists 
d30485a0025c: Pushed 
...
v1.1: digest: sha256:d79bf78670dbe957ccc9a53879513dec420f25119adf2d3614e5adf9281faa27 size: 856
```

---

## Задание 4. Описание многоконтейнерных приложений с помощью Docker Compose

### Ход выполнения работы

Исходный код файла task4/.env:
```
APP_PORT=5000
NGINX_PORT=8080
APP_TITLE=Задание 4: Docker Compose (Flask + Nginx + PostgreSQL)

POSTGRES_DB=app_db
POSTGRES_USER=app_user
POSTGRES_PASSWORD=app_password
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
  db:
    image: postgres:15-alpine
    container_name: compose-postgres-db
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - dbdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - backend-net

  app:
    image: nrashchynski/lab1-python-app:v1.1
    container_name: compose-flask-app
    environment:
      - APP_TITLE=${APP_TITLE}
      - DB_HOST=db
      - DB_NAME=${POSTGRES_DB}
      - DB_USER=${POSTGRES_USER}
      - DB_PASSWORD=${POSTGRES_PASSWORD}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - frontend-net
      - backend-net

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
      - frontend-net

volumes:
  dbdata:

networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge

```

Ход выполнения работы и консольный вывод:
Запуск сервисов в фоновом режиме:
```Bash
$ docker compose up -d
```
```
[+] up 19/19
 ✔ Image postgres:15-alpine     Pulled
 ✔ Network task4_backend-net    Created
 ✔ Volume task4_dbdata          Created
 ✔ Network task4_frontend-net   Created
 ✔ Container compose-postgres-db Healthy
 ✔ Container compose-flask-app   Started
 ✔ Container compose-nginx-proxy Started
 ```

 Проверка статуса контейнеров:
 ```Bash
 $ docker compose ps
 ```
 ```
NAME                  IMAGE                               COMMAND                  SERVICE   CREATED              STATUS                        PORTS
compose-flask-app     nrashchynski/lab1-python-app:v1.1   "python app.py"          app       About a minute ago   Up 57 seconds                 5000/tcp
compose-nginx-proxy   nginx:latest                        "/docker-entrypoint.…"   proxy     About a minute ago   Up 57 seconds                 0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
compose-postgres-db   postgres:15-alpine                  "docker-entrypoint.s…"   db        About a minute ago   Up About a minute (healthy)   5432/tcp
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
    <title>Задание 4: Docker Compose (Flask + Nginx + PostgreSQL)</title>
</head>
<body>
    <h1>Задание 4: Docker Compose (Flask + Nginx + PostgreSQL)</h1>
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
compose-postgres-db  | PostgreSQL init process complete; ready for start up.
compose-postgres-db  | 2026-09-24 13:46:18.296 UTC [1] LOG:  database system is ready to accept connections
compose-flask-app    |  * Running on [http://172.19.0.3:5000](http://172.19.0.3:5000)
compose-flask-app    | 172.18.0.3 - - [24/Sep/2026 13:47:44] "GET / HTTP/1.1" 200 -
compose-nginx-proxy  | 192.168.65.1 - - [24/Sep/2026:13:47:44 +0000] "GET / HTTP/1.1" 200 455 "-" "curl/8.7.1"
```

Остановка и удаление инфраструктуры:
```
$ docker compose down
```
[+] down 4/4
 ✔ Container compose-nginx-proxy Removed
 ✔ Container compose-flask-app   Removed
 ✔ Container compose-postgres-db Removed
 ✔ Network task4_frontend-net    Removed
 ✔ Network task4_backend-net     Removed
 ```

---

## Задание 5. Ограничение ресурсов контейнера и миграции базы данных (FastAPI + Liquibase + PostgreSQL)

### Исходный код проекта, конфигурации Docker Compose, миграции Liquibase в папке task5/

### Ход выполнения работы

Исходный код файла task5/.env:
```env
POSTGRES_DB=students_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgresql://postgres:postgres@db:5432/students_db
```

Исходный код файла task5/docker-compose.yml:
```
services:
  db:
    image: postgres:15-alpine
    container_name: students-postgres-db
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - dbdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - student-net

  liquibase:
    image: liquibase/liquibase:latest
    container_name: students-liquibase-migration
    depends_on:
      db:
        condition: service_healthy
    environment:
      - LIQUIBASE_COMMAND_URL=jdbc:postgresql://db:5432/${POSTGRES_DB}
      - LIQUIBASE_COMMAND_USERNAME=${POSTGRES_USER}
      - LIQUIBASE_COMMAND_PASSWORD=${POSTGRES_PASSWORD}
      - LIQUIBASE_COMMAND_CHANGELOG_FILE=changelog.xml
      - INSTALL_POSTGRESQL_DRIVER=true
    volumes:
      - ./changelog:/liquibase/changelog
      - ./drivers/postgresql.jar:/liquibase/internal/lib/postgresql.jar
    command: ["update"]
    networks:
      - student-net

  app:
    build: .
    container_name: students-fastapi-app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      db:
        condition: service_healthy
      liquibase:
        condition: service_completed_successfully
    networks:
      - student-net

volumes:
  dbdata:

networks:
  student-net:
    driver: bridge
```

Ход выполнения работы и консольный вывод:

Сборка и запуск сервисов с логированием выполнения миграций:
```
$ docker compose up --build
```
```
[+] Building 3.3s (12/12) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => CACHED [2/5] WORKDIR /app
 => CACHED [3/5] COPY requirements.txt .
 => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => CACHED [5/5] COPY ./app ./app
 => naming to docker.io/library/task5-app:latest

[+] up 5/5
 ✔ Image task5-app                Built
 ✔ Network task5_student-net      Created
 ✔ Container students-postgres-db Created
 ✔ Container students-liquibase-migration Created
 ✔ Container students-fastapi-app Created
Attaching to students-fastapi-app, students-liquibase-migration, students-postgres-db

students-postgres-db  | 2026-09-24 15:39:06.726 UTC [1] LOG:  starting PostgreSQL 15.19 on aarch64-unknown-linux-musl
students-postgres-db  | 2026-09-24 15:39:06.729 UTC [1] LOG:  database system is ready to accept connections
Container students-postgres-db Healthy

students-liquibase-migration  | Starting Liquibase at 15:39:12 using Java 21.0.11
students-liquibase-migration  | Liquibase Version: 5.0.4
students-liquibase-migration  | Database is up to date, no changesets to execute
students-liquibase-migration  | 
students-liquibase-migration  | UPDATE SUMMARY
students-liquibase-migration  | Run:                            0
students-liquibase-migration  | Previously run:                 1
students-liquibase-migration  | Filtered out:                   0
students-liquibase-migration  | -------------------------------
students-liquibase-migration  | Total change sets:              1
students-liquibase-migration  | 
students-liquibase-migration  | Liquibase command 'update' was executed successfully.
students-liquibase-migration exited with code 0

students-fastapi-app          | INFO:     Started server process [1]
students-fastapi-app          | INFO:     Waiting for application startup.
students-fastapi-app          | INFO:     Application startup complete.
students-fastapi-app          | INFO:     Uvicorn running on [http://0.0.0.0:8000](http://0.0.0.0:8000) (Press CTRL+C to quit)
```

Проверка статуса активных контейнеров после применения миграций:
```
$ docker compose ps
```
```
NAME                   IMAGE                COMMAND                  SERVICE   CREATED         STATUS                   PORTS
students-fastapi-app   task5-app            "uvicorn app.main:ap…"   app       2 minutes ago   Up 2 minutes             0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
students-postgres-db   postgres:15-alpine   "docker-entrypoint.s…"   db        2 minutes ago   Up 2 minutes (healthy)   5432/tcp
```

Остановка и удаление инфраструктуры:
```
$ docker compose down
```
```
[+] down 4/4
 ✔ Container students-fastapi-app        Removed
 ✔ Container students-liquibase-migration Removed
 ✔ Container students-postgres-db        Removed
 ✔ Network task5_student-net             Removed
 ```

 ---

## Задание 6. Настройка многосредовой инфраструктуры (Local, Dev, Prod), автоматизация через Makefile и интеграция LLM

### Ход выполнения работы

Описание конфигураций окружений:
- **Local (`compose.local.yaml`)**: Полнофункциональный стек для разработки, включающий FastAPI, PostgreSQL, Liquibase и сервис Ollama (`ollama/ollama:latest`) для локального запуска моделей машинного обучения.
- **Dev (`compose.dev.yaml`)**: Гибридная конфигурация для разработки с переопределенными переменными окружения (`.env.dev`) и портом приложения `8001`.
- **Prod (`compose.prod.yaml`)**: Продакшн-конфигурация с отдельными переменными окружения (`.env.prod`), портом `8002` и политикой автоматического перезапуска `restart: always`.

Автоматизация (Makefile):
Создан файл `Makefile`, содержащий сценарии управления всеми тремя окружениями:
```
PHONY: local-up local-down dev-up dev-down prod-up prod-down ps clean

local-up:
	docker compose --env-file .env -f compose.local.yaml up -d --build

local-down:
	docker compose -f compose.local.yaml down

dev-up:
	docker compose --env-file .env.dev -f compose.dev.yaml up -d --build

dev-down:
	docker compose -f compose.dev.yaml down

prod-up:
	docker compose --env-file .env.prod -f compose.prod.yaml up -d --build

prod-down:
	docker compose -f compose.prod.yaml down

ps:
	docker compose -f compose.local.yaml ps

clean:
	docker system prune -f
```

Результаты запуска и тестирование Ollama   
Запуск локального окружения:
```make local-up```
```
docker compose --env-file .env -f compose.local.yaml up -d --build
[+] up 5/5
 ✔ Image ollama/ollama:latest Pulled                                                                             1053.7s
[+] Building 6.6s (12/12) FINISHED                                                                                      
 => [internal] load local bake definitions                                                                         0.0s
 => => reading from stdin 538B                                                                                     0.0s
 => [internal] load build definition from Dockerfile                                                               0.0s
 => => transferring dockerfile: 253B                                                                               0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                6.3s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [1/5] FROM docker.io/library/python:3.11-slim@sha256:da047cb8f9d1d98e5c070f5300ba9f7274e33b8fc0e5be5ed88740ae  0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:da047cb8f9d1d98e5c070f5300ba9f7274e33b8fc0e5be5ed88740ae  0.0s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 6.75kB                                                                                0.0s
 => CACHED [2/5] WORKDIR /app                                                                                      0.0s
 => CACHED [3/5] COPY requirements.txt .                                                                           0.0s
 => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt                                                0.0s
 => CACHED [5/5] COPY ./app ./app                                                                                  0.0s
 => exporting to image                                                                                             0.0s
 => => exporting layers                                                                                            0.0s
 => => exporting manifest sha256:b7216165722eb71320b667f24ca54feda9da87c1e3bfb6af18256c172c095329                  0.0s
 => => exporting config sha256:90fa5b15ab6a76189be94032f1a24f35a16a8305ac92a98356be3d99c7df72e8                    0.0s
 => => exporting attestation manifest sha256:8e973e921418ca5bac56077e41a1f949484a5ebecb1f22951570fcff8fdf8414      0.0s
 => => exporting manifest list sha256:f3a5bf83c5c2bf36e168cb0344fb05bd07918aec72beeba15ab8d20904903922             0.0s
 => => naming to docker.io/library/task6-app:latest                                                                0.0s
[+] up 13/13king to docker.io/library/task6-app:latest                                                             0.0s
 ✔ Image ollama/ollama:latest                   Pulled                                                           1053.7s
 ✔ Image task6-app                              Built                                                               6.7s
 ✔ Network task6_student-net                    Created                                                             0.0s
 ✔ Volume task6_ollama_data                     Created                                                             0.0s
 ✔ Volume task6_dbdata_local                    Created                                                             0.0s
 ✔ Container students-postgres-db-local         Healthy                                                             6.5s
 ✔ Container students-ollama-llm                Started                                                             0.4s
 ✔ Container students-liquibase-migration-local Exited                                                             11.3s
 ✔ Container students-fastapi-app-local         Started                                                            11.3s
```

**Статус запущенных контейнеров:**
```make ps:```
```
NAME                         IMAGE                  COMMAND                  SERVICE   STATUS              PORTS
students-fastapi-app-local   task6-app              "uvicorn app.main:ap…"   app       Up                  0.0.0.0:8000->8000/tcp
students-ollama-llm          ollama/ollama:latest   "/bin/ollama serve"      ollama    Up                  0.0.0.0:11434->11434/tcp
students-postgres-db-local   postgres:15-alpine     "docker-entrypoint.s…"   db        Up (healthy)        5432/tcp
```

**Тестирование модели `tinyllama` в контейнере Ollama:**
```text
nazar@MacBook-Air-Nazar task6 % docker exec -it students-ollama-llm ollama run tinyllama
```
```
pulling manifest 
verifying sha256 digest 
writing manifest 
success 
>>> Hello
I'm glad to be of help! If you have any more questions, feel free to ask. I'm always happy to provide more 
detailed information and answer any questions you may have. Have a great day!
>>> /bye
What's next:
    Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug students-ollama-llm
    Learn more at https://docs.docker.com/go/debug-cli/
```

Проверка API Ollama:
```
curl http://localhost:11434/api/tags
```
```
{"models":[{"name":"tinyllama:latest","model":"tinyllama:latest","modified_at":"2026-09-25T12:53:40.297500004Z","size":637700138,"digest":"2644915ede352ea7bdfaff0bfac0be74c719d5d5202acb63a6fb095b52f394a4","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama"],"parameter_size":"1B","quantization_level":"Q4_0","context_length":2048,"embedding_length":2048},"capabilities":["completion"]}]}%   
```

Остановка стека:
```
make local-down
```
```
docker compose -f compose.local.yaml down
[+] down 5/5
 ✔ Container students-fastapi-app-local         Removed                                                             0.4s
 ✔ Container students-ollama-llm                Removed                                                             0.1s
 ✔ Container students-liquibase-migration-local Removed                                                             0.0s
 ✔ Container students-postgres-db-local         Removed                                                             0.1s
 ✔ Network task6_student-net                    Removed                                                             0.1s
 ```

---

## Ответы на контрольные вопросы

#### 1. Что такое Docker и зачем он нужен? В чём ключевые преимущества для разработки и эксплуатации? Какие есть альтернативные системы контейнеризации и в каких сценариях они предпочтительнее (например, Podman, containerd)?
* **Docker** — это платформа контейнеризации, позволяющая упаковывать приложение со всеми его зависимостями, библиотеками и конфигурациями в изолированный контейнер.
* **Преимущества:**
  * **Разработка:** одинаковая среда у всех разработчиков, быстрый запуск окружения ("работает везде, где есть Docker").
  * **Эксплуатация:** изолированность сервисов, эффективное использование ресурсов ОС (в отличие от тяжелых виртуальных машин), простота масштабирования и автоматизации CI/CD.
* **Альтернативы:**
  * **Podman:** не требует демона (`daemonless`), работает от имени обычного пользователя (`rootless`), совместим по CLI с Docker. Предпочтителен в корпоративных средах с строгой политикой безопасности.
  * **containerd / CRI-O:** низкоуровневые среды исполнения контейнеров. Используются внутри Kubernetes вместо полного Docker Engine для уменьшения накладных расходов.

#### 2. Что такое Docker‑образ? Как его получить (из реестра, через сборку, из контейнера)? В чём разница между образом и контейнером?
* **Docker-образ (Image)** — это неизменяемый шаблон (шаблон файловой системы с инструкциями), состоящий из набора слоев «только для чтения» (read-only).
* **Как получить:**
  1. Из реестра: `docker pull nginx:latest`
  2. Через сборку из Dockerfile: `docker build -t my-app .`
  3. Из запущенного контейнера: `docker commit <container_id> my-new-image`
* **Разница:** Образ — это «чертеж/пассивный файл» на диске, а контейнер — это запущенный и изолированный экземпляр данного образа (процесс в ОС с тонким изменяемым слоем записи `read-write`).

#### 3. Как запустить контейнер? Как пробросить порты, чтобы получить доступ к сервису снаружи? Как задать имя контейнера и ограничить ресурсы (CPU/RAM)?
* **Запуск:** `docker run -d --name my_app nginx`
* **Проброс портов (`-p`):** `docker run -d -p 8080:80 nginx` (порт `8080` хоста мапится на порт `80` внутри контейнера).
* **Имя контейнера (`--name`):** `docker run --name custom_name nginx`
* **Ограничение ресурсов:** `docker run -d --memory="512m" --cpus="1.5" nginx` (ограничение до 512 МБ ОЗУ и 1.5 ядра CPU).

#### 4. Как просмотреть логи контейнера? Как фильтровать логи по времени, по строкам, по уровню (например, ошибки)? Как настроить ротацию логов?
* **Просмотр логов:** `docker logs <container_name>` (с флагом `-f` — в режиме реального времени).
* **Фильтрация:**
  * По времени: `docker logs --since "2026-09-25T10:00:00" --until "1h" <container_name>`
  * По строкам: `docker logs --tail 100 <container_name>`
  * По уровню/тексту: через утилиту grep, например `docker logs <container_name> 2>&1 | grep "ERROR"`
* **Ротация логов:** Настраивается в `/etc/docker/daemon.json` через параметры `log-driver: "json-file"` и `log-opts` (`max-size: "10m"`, `max-file: "3"`).

#### 5. Как сохранить данные внутри контейнера между перезапусками? В чём разница между volume, bind mount и tmpfs? Как правильно выбрать тип хранения для базы данных, кеша, логов?
* **Volume:** Данные управляются Docker и хранятся в специальной директории хоста (`/var/lib/docker/volumes/`). **Выбор:** Базы данных (PostgreSQL, MySQL).
* **Bind mount:** Привязка произвольной папки или файла с хостовой системы в контейнер. **Выбор:** Исходный код при разработке, внешние конфиги.
* **tmpfs:** Данные хранятся только в оперативной памяти хоста (не пишутся на диск). **Выбор:** Кратковременный кеш, секретные данные/ключи.

#### 6. Как подключить контейнеры к одной сети? Какие типы сетей бывают (bridge, host, overlay) и для чего используется каждая? Какие есть альтернативы (например, без сетей Docker)?
* **Подключение:** `docker network create my_net`, затем `docker run --network my_net ...`
* **Типы сетей:**
  * **bridge (по умолчанию):** изолированная программная сеть на одном хосте, контейнеры видят друг друга по именам/IP.
  * **host:** контейнер использует сетевой стек хост-системы без изоляции.
  * **overlay:** объединяет несколько хостов Docker Swarm в единую сеть.
  * **none:** полностью отключает сетевой стек контейнера.
* **Альтернативы:** Использование системных сетевых интерфейсов хоста напрямую или настроек `macvlan`/`ipvlan`.

#### 7. Почему контейнеры могут обращаться друг к другу по имени? Как Docker разрешает имена внутри сети (DNS, service discovery)? Что происходит, если имя сервиса меняется или контейнер перезапускается?
* В пользовательских сетях (`user-defined bridge`) Docker запускает встроенный **DNS-сервер** (`127.0.0.11`).
* DNS-сервер сопоставляет имя контейнера (или алиас сервиса) с его текущим внутренним IP-адресом.
* Если контейнер перезапускается и получает новый IP-адрес, внутренний DNS автоматически обновляет запись, поэтому обращение по имени продолжается без сбоев.

#### 8. Что такое метки (docker tag)? Как правильно добавлять метки образам (семантика, latest vs конкретные теги, best practices)? Как удалить теги и чем это отличается от удаления образов?
* **Метка (tag)** — это текстовый указатель (алиас) на конкретный ID образа (`registry/repository:tag`).
* **Best Practices:** Использовать семантическое версионирование (`1.2.3`), хеш Git-коммита (`app:a1b2c3d`). Избегать использования `:latest` в Production, так как этот тег не гарантирует неизменяемость сборки.
* **Удаление:** `docker rmi image:tag` удаляет лишь конкретную метку-ссылку. Сам образ (файлы слоев) удалится только тогда, когда у него не останется ни одного тега.

#### 9. Как удалить ненужные образы и контейнеры? Как автоматизировать очистку (команды, скрипты, политики)? Как избежать случайного удаления работающих контейнеров?
* **Удаление вручную:** `docker rm <id>` (контейнеры), `docker rmi <id>` (образы).
* **Автоматическая очистка:** `docker system prune -a --volumes` (удаляет остановленные контейнеры, неиспользуемые сети и образы).
* **Защита от удаления:** Команда `docker rm` по умолчанию не удаляет запущенные контейнеры (требует флаг `-f`). Для одноразовых задач используется флаг `--rm` при запуске (`docker run --rm ...`).

#### 10. Как выполнить команду внутри работающего контейнера? В чём разница между docker exec и docker attach? Когда лучше использовать entrypoint/cmd вместо exec?
* **Выполнение команды:** `docker exec -it <container_id> bash`
* **Разница:**
  * `docker exec` создает **новый** отдельный процесс внутри уже работающего контейнера.
  * `docker attach` подключается к **главному (PID 1)** процессу контейнера (к его stdout/stdin/stderr).
* **Применение:** `ENTRYPOINT`/`CMD` задают основной жизненный цикл контейнера при его старте, а `exec` используется для отладки, ручного обслуживания и проведения проверок.

#### 11. Как узнать, какие файлы изменяет программа внутри контейнера? Как сравнить слои образа? Как получить diff изменений в файловой системе контейнера?
* **Просмотр изменений:** `docker diff <container_name>` — показывает добавленные (A), измененные (C) и удаленные (D) файлы относительно базового образа.
* **Сравнение слоев:** С помощью команды `docker history <image_name>` или сторонней утилиты `dive`.

#### 12. Когда происходит завершение контейнера? Как корректно остановить контейнер (graceful shutdown)? Как настроить сигналы остановки (stop_grace_period) и обработку SIGTERM?
* Контейнер завершается, когда завершает работу его основной процесс (PID 1).
* **Graceful shutdown:** Команда `docker stop` отправляет сигнал `SIGTERM` процессу PID 1, ждет таймаут (по умолчанию 10 секунд), и если процесс не завершился — принудительно отправляет `SIGKILL`.
* **Настройка:** В Dockerfile директива `STOPSIGNAL` задает отправляемый сигнал. В Docker Compose параметр `stop_grace_period: 30s` увеличивает время ожидания корректного завершения.

#### 13. Как работает кеширование слоев при сборке образа? Почему важен порядок инструкций в Dockerfile для ускорения пересборки? Объясните причины ускорения/замедления: кеш слоёв, порядок инструкций, multi‑stage, .dockerignore. Как измерить время сборки и как понять, какой слой пересобирался?
* Каждый шаг в Dockerfile создает слой. При сборке Docker проверяет, изменились ли исходные файлы и команды. Если изменений нет, используется сохраненный **кеш слоя**.
* **Порядок:** Инструкции, меняющиеся редко (установка пакетов `apt`, `pip install`), нужно ставить в начало, а постоянно изменяющийся исходный код (`COPY . .`) — в самый конец.
* `.dockerignore` исключает лишние файлы (папку `.git`, `node_modules`, временные файлы), предотвращая сброс кеша.
* **Измерение:** Переменная `DOCKER_BUILDKIT=1 docker build ...` показывает прогресс сборки, подпись `CACHED` указывает на использование кеша слоя.

#### 14. К какому количеству слоёв стремиться в образе? Какие правила оптимизации слоёв (объединение RUN, порядок инструкций, очистка кеша менеджера пакетов)? Как оценить размер образа и его состав (слои, файлы)?
* Следует стремиться к минимальному количеству и минимальному размеру слоев.
* **Правила:**
  1. Объединять команды `RUN` через `&&` (например: `apt-get update && apt-get install -y pkg && rm -rf /var/lib/apt/lists/*`).
  2. Очищать кеш менеджеров пакетов в том же слое `RUN`, где они устанавливались.
* **Оценка размера:** `docker image ls` (общий размер), `docker history <image>` (размер каждого слоя).

#### 15. Опишите базовые команды Dockerfile: FROM, RUN, COPY, ADD, WORKDIR, ENV, EXPOSE, CMD, ENTRYPOINT. Что они делают, какие есть частые ошибки и антипаттерны? Где смотреть официальную документацию и как проверять Dockerfile на ошибки (hadolint)?
* **FROM:** Задает базовый образ.
* **RUN:** Выполняет команду во время сборки и создает новый слой.
* **COPY / ADD:** Копируют файлы в образ.
* **WORKDIR:** Устанавливает рабочую директорию.
* **ENV:** Задает переменные окружения.
* **EXPOSE:** Документирует используемый порт.
* **CMD / ENTRYPOINT:** Задают команду запуска контейнера.
* **Антипаттерны:** Запуск процессов от `root`, использование `:latest`, отсутствие очистки кеша пакетов.
* **Проверка:** Документация на docs.docker.com, статическая проверка ошибок с помощью линтера **Hadolint** (`hadolint Dockerfile`).

#### 16. Что такое контекст сборки? Как он передаётся в Docker и как влияет на COPY/ADD? Как оптимизировать контекст (размер, .dockerignore), чтобы ускорить сборку и уменьшить размер образа?
* **Контекст сборки** — это директория (и её содержимое), передаваемая демону Docker при выполнении `docker build <path>`.
* Огромный контекст долго передается демону.
* **Оптимизация:** Создание файла `.dockerignore`, куда записываются кэши, виртуальные окружения, временные файлы и крупные медиафайлы, не требующиеся для сборки.

#### 17. В чем разница между COPY и ADD? Когда нужно использовать ADD?
* **COPY:** Прозрачно копирует файлы и директории с хост-системы в контейнер.
* **ADD:** Помимо обычного копирования, умеет автоматически распаковывать локальные архивы (`tar`, `tar.gz`) и скачивать файлы по URL.
* **Правило:** Рекомендуется всегда использовать `COPY`. `ADD` стоит использовать только для автораспаковки локальных тарболов.

#### 18. В чем разница между CMD и ENTRYPOINT? Как они взаимодействуют друг с другом?
* **ENTRYPOINT:** Задает исполняемый файл или команду, которая будет выполняться **всегда** при запуске контейнера.
* **CMD:** Задает параметры по умолчанию для `ENTRYPOINT` или команду по умолчанию (если `ENTRYPOINT` не задан).
* **Взаимодействие:** Конструкция `ENTRYPOINT ["python3", "app.py"]` + `CMD ["--port", "8000"]` позволяет при запуске переопределять только аргументы `CMD` через `docker run my_image --port 9000`.

#### 19. В чем разница между ARG и ENV? Доступны ли ARG во время выполнения контейнера?
* **ARG (Build Arguments):** Переменная, доступная **только во время сборки** образа. Не сохраняется и **не доступна** в запущенном контейнере.
* **ENV (Environment Variables):** Переменная окружения, доступная как во время сборки, так и во время работы контейнера.

#### 20. Что такое Multi-stage builds (многоэтапная сборка)? Приведите пример, когда это необходимо (например, сборка Go/React приложения и копирование только бинарника в финальный образ).
* **Multi-stage builds** — подход с использованием нескольких инструкций `FROM` в одном Dockerfile.
* **Зачем нужен:** Позволяет собрать приложение в тяжелом образе (с компиляторами и SDK), а в финальный минималистичный образ скопировать только готовый скомпилированный бинарник или статическую сборку.
* **Пример:**
  ```dockerfile
  # Этап 1: Сборка Go-приложения
  FROM golang:1.22 AS builder
  WORKDIR /app
  COPY . .
  RUN CGO_ENABLED=0 GOOS=linux go build -o myapp .

  # Этап 2: Финальный минимальный образ
  FROM alpine:latest
  WORKDIR /root/
  COPY --from=builder /app/myapp .
  CMD ["./myapp"]
  ```
#### 21. Из каких компонентов состоит Docker Engine?
1. **Docker Daemon (`dockerd`):** Фоновый процесс, управляющий объектами (образы, контейнеры, тома, сети).
2. **Docker Engine REST API:** Интерфейс взаимодействия с демоном.
3. **Docker CLI (`docker`):** Интерфейс командной строки для пользователя.
4. **containerd & runc:** Низкоуровневые компоненты стандарта OCI для непосредственного запуска процессов контейнера.

#### 22. Как посмотреть подробную информацию о контейнере (IP-адрес, смонтированные volumes, переменные окружения)? Привести примеры команды.
Используется команда `docker inspect`:
* **Все данные:** `docker inspect <container_name>`
* **Получить IP-адрес:**
  ```bash
  docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>
  ```
* **Посмотреть смонтированные Volumes:**
  ```
  docker inspect -f '{{json .Mounts}}' <container_name>
  ```

#### 23. Как посмотреть потребление ресурсов (CPU, RAM) контейнером в реальном времени?
Используется команда:
```
docker stats
```
Или для конкретного контейнера без непрерывного потока:
```
docker stats --no-stream <container_name>
```

#### 24. Основные возможности Docker Compose: сервисы, тома, сети, секреты, профили, зависимости. В чём отличие между docker-compose (отдельный бинарный файл) и docker compose (модуль)? Какие возможности есть только в новом модуле?
* **Возможности Compose: декларативное описание стека сервисов (services), объединенных сетями (networks), томами (volumes), секретами (secrets), профилями запуска (profiles) и зависимостями (depends_on).**
* **Отличие:**
  * **docker-compose (V1) — устаревший бинарник на Python.**
  * **docker compose (V2) — плагин, интегрированный напрямую в Docker CLI на языке Go (быстрее, поддерживается разработчиками).**
* **В V2 добавлены: команда docker compose watch, полная интеграция с механизмом BuildKit и спецификацией Compose Specification.**

#### 25. Как в Docker Compose настроить порядок запуска сервисов с учетом их готовности?
Используется секция depends_on с параметром condition: service_healthy совместно с блоком healthcheck:
```
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

#### 26. Что такое Healthcheck в Docker и Docker Compose? Как он работает и зачем нужен?
* Healthcheck — инструкция/механизм периодической проверки работоспособности сервиса внутри контейнера (например, выполнением команды curl или SQL-запроса).
* Статусы: starting $\rightarrow$ healthy (или unhealthy).
* Зачем нужен: позволяет оркестратору или Docker Compose понимать, действительно ли приложение внутри контейнера готово принимать трафик, а не просто запустило процесс.

#### Как переопределить или дополнить базовый compose.yaml (docker-compose.yml) файл для разных окружений (dev, prod)?
Используются несколько файлов конфигураций:
1. Базовый compose.yaml с общей логикой.
2. Файл переопределения compose.override.yaml (автоматически подтягивается для Dev).
3. Файл для прод-среды compose.prod.yaml.
* Запуск с явным объединением файлов:
```
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

#### 28. Почему запускать процессы от имени root внутри контейнера — плохая практика? Как запустить контейнер от непривилегированного пользователя (non-root)?
* Опасность: При некорректной изоляции или уязвимости Docker («побег из контейнера») злоумышленник получит права root на самой хост-системе.
* Запуск от non-root:
  1. В Dockerfile создать пользователя и группу:
     ```
     RUN addgroup -S appgroup && adduser -S appuser -G appgroup
	 USER appuser
     ```
  2. Или при запуске через CLI/Compose: docker run --user 1000:1000 ...

#### 29. Как сделать файловую систему контейнера доступной только для чтения (read-only)? Как при этом работать с временными файлами?
* Запуск в Read-Only: Флаг --read-only в CLI или параметр read_only: true в Compose.
* Временные файлы: Для каталогов, требующих записи (например, /tmp или /run), монтируется хранилище в RAM через tmpfs:
  ```
  services:
  app:
    image: myapp
    read_only: true
    tmpfs:
      - /tmp
      - /run
  ```

#### 30. Как безопасно передавать секреты (пароли, ключи API) в Docker и Docker Compose?
* Сверху вниз по безопасности:
  1. Docker Secrets / Compose Secrets: Передача секретов через монтируемые файлы в памяти (/run/secrets/secret_name), доступные только конкретным сервисам.
  2. .env файлы: Использование файла .env (который внесен в .gitignore) для проброса переменных окружения без явного хардкода в файлы конфигураций.
* Антипаттерн: Хардкодить секреты в Dockerfile, передавать их через ARG или публиковать в Docker Hub.

#### Какие ограничения имеет Docker Compose при работе в Production? Почему для кластеров используют оркестраторы (Kubernetes, Docker Swarm)?
* Ограничения Compose: Работает только на одной физической/виртуальной машине (одноузловой), не умеет автоматически перезапускать упавшие узлы кластера, распределять нагрузку между серверами, выполнять Rolling Updates без простоя и масштабироваться на сотни серверов.
* Зачем оркестраторы: Kubernetes и Swarm обеспечивают отказоустойчивость, самовосстановление (self-healing), автомасштабирование и балансировку нагрузки в распределенном кластере серверов.

#### Что такое Docker Swarm? Чем он отличается от Kubernetes?
* Docker Swarm — встроенный в Docker инструмент оркестрации контейнерных кластеров.
* Сравнение:
  1. Docker Swarm: Прост в настройке, использует стандартный CLI и Compose-файлы, идеален для небольших и средних проектов. Имеет меньшую функциональность
  2. Kubernetes (K8s): Де-факто стандарт индустрии с огромной экосистемой, гибким управлением ресурсами и сложной архитектурой. Требует больших затрат на настройку и поддержку, предназначен для крупных микросервисных систем.
