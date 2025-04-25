from .models import *
from django.db import transaction


class PerevalDatabase:
    """
    Класс для работы с базой данных перевалов.
    Предоставляет метод для создания записи о перевале с привязкой к пользователю, координатам и изображениям.
    """

    @staticmethod
    @transaction.atomic
    def create_pereval(data):
        # Извлекаем и обрабатываем данные пользователя, координат и изображений
        user_data = data.pop('user')
        coords_data = data.pop('coords')
        images_data = data.pop('images')

        # Получаем или создаём пользователя,
        user, created = PerevalUser.objects.get_or_create(email=user_data['email'], defaults=user_data)
        # Создаём запись о координатах
        coords = PerevalCoords.objects.create(**coords_data)
        # Создаём запись о перевале
        pereval = PerevalAdded.objects.create(user=user, coords=coords, **data)

        # Создаём запись о координатах
        for img in images_data:
            PerevalImage.objects.create(pereval=pereval, title=img['title'], image_url=img['image_url'])

        return pereval