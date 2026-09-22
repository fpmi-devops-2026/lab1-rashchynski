FROM nginx:alpine

# Копируем созданный HTML-файл в стандартную директорию Nginx
COPY index.html /usr/share/nginx/html/index.html

# Открываем 80 порт
EXPOSE 80

# Запускаем Nginx в фоновом режиме
CMD ["nginx", "-g", "daemon off;"]
