# FSTR API — REST-сервис для добавления перевалов

## Описание проекта

REST API для приёма и хранения информации о перевалах в рамках проекта ФСТР (Федерация спортивного туризма России).  
Сервис предоставляет возможность:

- Отправлять информацию о перевале (`POST`)
- Получать список перевалов по email пользователя (`GET`)
- Получать подробную информацию о перевале по его ID (`GET`)
- Обновлять данные перевала, если его статус — `"new"` (`PATCH`)

Документация автоматически доступна через Swagger и ReDoc.

## Используемые технологии

- Python 3.12  
- Django 5.2  
- Django REST Framework  
- PostgreSQL — база данных  
- psycopg2-binary — драйвер PostgreSQL  
- drf-yasg — автогенерация Swagger / ReDoc  
- django-filter — фильтрация в API  
- python-dotenv — хранение конфиденциальных данных в .env  

## Структура проекта

- `submitData/PerevalBase/pereval/models.py` — модели пользователя, перевала, координат и изображений  
- `submitData/PerevalBase/pereval/serializers.py` — сериализаторы для POST/GET/PATCH  
- `submitData/PerevalBase/pereval/views.py` — реализация логики API  
- `submitData/PerevalBase/pereval/urls.py` — маршруты приложения  
- `submitData/PerevalBase/PerevalBase/settings.py` — настройки проекта с подключением .env  
- `submitData/PerevalBase/PerevalBase/urls.py` — главные маршруты проекта  

## Установка и запуск проекта

1. Клонировать репозиторий:
```bash
git clone https://github.com/Vasineva/submitData
cd submitData
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate   # для Windows
```

3. Перейдите в папку PerevalBase и установите зависимости:
```bash
cd PerevalBase
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта PerevalBase/ (на одном уровне с settings.py) и заполните его следующими данными:
```ini
FSTR_DB_NAME=your_db_name  # имя БД
FSTR_DB_LOGIN=your_db_user  # имя пользователя
FSTR_DB_PASS=your_db_password  # пароль
FSTR_DB_HOST=localhost
FSTR_DB_PORT=port # Обычно порт для PostgreSQL — 5432
```

5. Применить миграции и запустить сервер:
```bash
python manage.py migrate
python manage.py runserver
```

## Документация API

После запуска проекта, API-документация доступна по адресам:

- Swagger UI: http://localhost:8000/swagger/  
- ReDoc: http://localhost:8000/redoc/

## Основные эндпоинты

 - POST   `/api/submitData/` - Добавить новый перевал
 - GET    `/api/submitData/?user__email=example@mail.ru` - Получить список перевалов по email 
 - GET    `/api/submitData/<id>/` -  Получить информацию о перевале по ID 
 - PATCH  `/api/submitData/<id>/` - Обновить перевал (если status = "new") 

## Пример POST-запроса

```json
{
  "beauty_title": "пер.",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22 13:18:13",
  "user": {
           "email": "qwerty@mail.ru",
           "fam": "Пупкин",
           "name": "Василий",
           "otc": "Иванович",
           "phone": "+7 555 55 55"
   },
   "coords": {
              "latitude": "45.3842",
              "longitude": "7.1525",
              "height": "1200"
   },
   "level": {
             "winter": "",
             "summer": "1А",
             "autumn": "1А",
             "spring": ""
    },
    "images": [
         {"title": "Седловина", "image_url": "http://example.com/image1.jpg"},
         {"title": "Подъем", "image_url": "http://example.com/image2.jpg"}
     ]
}
```

##  Ограничения

- Перевал можно редактировать только если его статус — `"new"`.
- Для создания перевала требуется, чтобы пользователь с указанным email уже существовал или был создан вместе с перевалом.

## Контакты

Разработчик: Екатерина  
Email: vasineva@email.com

---

Проект выполнен в рамках учебного задания школы Skillfactory для Федерации спортивного туризма России (ФСТР).
