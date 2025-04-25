import os
from dotenv import load_dotenv
from django.conf import settings
from .serializers import *
from rest_framework.exceptions import ValidationError

# Загружаем переменные окружения для подключения к базе данных
load_dotenv()

# Подключение к базе данных через переменные окружения
DB_HOST = os.getenv("FSTR_DB_HOST")
DB_PORT = os.getenv("FSTR_DB_PORT")
DB_USER = os.getenv("FSTR_DB_LOGIN")
DB_PASS = os.getenv("FSTR_DB_PASS")
DB_NAME = os.getenv("FSTR_DB_NAME")


settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

class PerevalDatabaseHandler:
    def add_user(self, user_data):
        serializer = PerevalUserSerializer(data=user_data)
        if serializer.is_valid():
            user_instance = serializer.save()
            print("Пользователь добавлен успешно!")
            return user_instance
        else:
            raise ValidationError(f"Ошибка валидации пользователя: {serializer.errors}")

    def add_coords(self, coords_data):
        serializer = PerevalCoordsSerializer(data=coords_data)
        if serializer.is_valid():
            coords_instance = serializer.save()
            print("Координаты добавлены успешно!")
            return coords_instance
        else:
            raise ValidationError(f"Ошибка валидации координат: {serializer.errors}")

    def add_pereval(self, pereval_data):
        serializer = PerevalAddedSerializer(data=pereval_data)
        if serializer.is_valid():
            pereval_instance = serializer.save()
            print("Перевал добавлен успешно!")
            return pereval_instance
        else:
            raise ValidationError(f"Ошибка валидации перевала: {serializer.errors}")

    def add_image(self, pereval_id, image_data):
        image_data['pereval'] = pereval_id
        serializer = PerevalImageSerializer(data=image_data)
        if serializer.is_valid():
            image_instance = serializer.save()
            print("Изображение добавлено успешно!")
            return image_instance
        else:
            raise ValidationError(f"Ошибка валидации изображения: {serializer.errors}")