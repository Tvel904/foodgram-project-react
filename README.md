#  Проект foodgram

## Описание проекта

Добро пожаловать в мир вкуса - в наш новый проект Foodgram. Тут вы сможете найти миллионы вкуснейших рецептов блюд, а также делиться и своими любимыми рецептами! Функционал проекта позволяет искать рецепты по тегам, добавлять любой рецепт себе в избранное, подписываться на авторов с вашими любимыми блюдами и многое другое! 
А главное - нажав на одну кнопку, вы можете добавить ингридиенты любого рецепта (или нескольких сразу) себе в список покупок, и скачать его файлом, чтобы идти в магазин и понимать, сколько точно нужно того или иного продукта.
Наслаждайтесь, и приятного аппетита!

## Технологии

Проект построен на следующих технологиях:
```yaml
Backend - Python==3.9, Django==3.2, djangorestframework==3.14, PostgreSQL==13.10
Frontend - JavaScript, HTML, CSS, React
Серверная часть - Nginx, Ubuntu, Docker
```
## Как развернуть проект локально

1. Клонировать код себе с github
    ```git@github.com:Tvel904/foodgram-project-react.git```

2. При запущенном Docker использовать следующие команды:
```yaml
    docker compose -f docker-compose.production.yml up -d
    docker compose -f docker-compose.production.yml exec backend python manage.py migrate
    docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
    docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/

    Также для загрузки в БД предустановленных ингредиентов, используйте следующую команду:
    docker compose -f docker-compose.production.yml exec backend python manage.py loaddata ingredients.json
```

## Как заполнить env

Конфигурация .env выглядит следующим образом:
```yaml
    POSTGRES_DB=***
    POSTGRES_USER=***
    POSTGRES_PASSWORD=***
    DB_HOST=***
    DB_PORT=***
    SECRET_KEY=***
    ALLOWED_HOSTS=***
    DEBUG=***
```

## Для теста проекта на рабочем сервере

Заходите на сайт *https://foodgramforfood.hopto.org*;

## Автор данного чуда

Ваш покорный слуга - **tvel904** (Соколов Денис) 
