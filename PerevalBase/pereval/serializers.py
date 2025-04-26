"""
Сериализаторы преобразуют данные моделей PerevalUser, PerevalCoords,
PerevalImage и PerevalAdded в формат, удобный для API. Сериализаторы обрабатывают
всю необходимую информацию, включая данные пользователя, координаты перевала и изображения.
"""

from .models import *
from rest_framework import serializers


class PerevalUserSerializer(serializers.ModelSerializer):
   class Meta:
       model = PerevalUser
       fields = '__all__'

class PerevalCoordsSerializer(serializers.ModelSerializer):
   class Meta:
       model = PerevalCoords
       fields = '__all__'

class PerevalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImage
        fields = ['title', 'image_url'] # # Здесь image_url будет хранить ссылку на изображения


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = PerevalUserSerializer()
    coords = PerevalCoordsSerializer()
    images = PerevalImageSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
            'user', 'coords',
            'level_winter', 'level_summer', 'level_autumn', 'level_spring',
            'images'
        ]

    def create(self, validated_data):
        # Извлекаем вложенные данные
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images')

        # Находим существующего пользователя или используем его
        user = PerevalUser.objects.get(email=user_data['email'])

        # Создаем координаты
        coords = PerevalCoords.objects.create(**coords_data)

        # Создаем сам перевал
        pereval = PerevalAdded.objects.create(user=user, coords=coords, **validated_data)

        # Создаем изображения и связываем их с перевалом
        for image_data in images_data:
            PerevalImage.objects.create(pereval=pereval, **image_data)

        return pereval




