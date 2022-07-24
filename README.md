# Foodgram - «Продуктовый помощник»

Foodgram, «Продуктовый помощник» - онлайн-сервис и API для него.

## Описание

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Использованные технологии

* Python 3.9
* Django 3.2.14
* Django Rest Framework 3.12.4
* Simple-JWT 4.8.0
* Docker 20.10
* Nginx 1.18

## Запуск проекта:

### Клонировать репозиторий и перейти в него в командной строке:

```python
git@github.com:yorriyurri/foodgram-project-react.git
cd foodgram-project-react/backend/foodgram
```

### Перейти в директорию infra/ и запустить docker-compose:

```python
cd infra/
docker-compose up
```

### Cоздать и активировать виртуальное окружение:

```python
python -m venv venv
source venv/scripts/activate
```

### Установить зависимости из файла requirements.txt:

```python
pip install -r requirements.txt
```

### Выполнить миграции:

```python
python manage.py migrate
```

## Примеры

Подробная документация API с примерами размещена по адресу:
http://127.0.0.1:8000/redoc/

## Автор

Студент 29 когорты Факультета Бэкэнд-разработки, Яндекс.Практикум:

* Ивайкин Юрий