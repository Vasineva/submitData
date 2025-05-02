"""
Сериализаторы преобразуют данные моделей в формат, удобный для REST API,
и обратно — для сохранения в базу данных.

- PerevalUserSerializer: сериализует пользователя, создаёт нового при необходимости (по email).
- PerevalCoordsSerializer: сериализует координаты перевала.
- PerevalImageSerializer: сериализует изображения перевала (название и ссылка).
- PerevalAddedSerializer: сериализует перевал с вложенными данными (user, coords, images),
  создаёт связанные объекты.
- PerevalInfoSerializer: используется для отображения полной информации о перевале (GET).
- PerevalCoordsUpdateSerializer: для частичного обновления координат.
- PerevalUpdateSerializer: для обновления перевала (если статус = 'new');
  обновляет поля, координаты и изображения.
"""

from .models import *
from rest_framework import serializers


class PerevalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']

    def create(self, validated_data):
        # Пытаемся найти пользователя по email
        user, created = PerevalUser.objects.get_or_create(
            email=validated_data['email'],
            defaults={
                'fam': validated_data.get('fam', ''),
                'name': validated_data.get('name', ''),
                'otc': validated_data.get('otc', ''),
                'phone': validated_data.get('phone', ''),
            }
        )
        return user

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

        # # Создаём или находим пользователя
        user_serializer = PerevalUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Создаем координаты
        coords = PerevalCoords.objects.create(**coords_data)

        # Создаем сам перевал
        pereval = PerevalAdded.objects.create(user=user, coords=coords, **validated_data)

        # Создаем изображения и связываем их с перевалом
        for image_data in images_data:
            PerevalImage.objects.create(pereval=pereval, **image_data)

        return pereval

class PerevalInfoSerializer(serializers.ModelSerializer):
    user = PerevalUserSerializer()
    coords = PerevalCoordsSerializer()
    images = PerevalImageSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
            'status', 'user', 'coords',
            'level_winter', 'level_summer', 'level_autumn', 'level_spring',
            'images'
        ]

class PerevalCoordsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalCoords
        fields = ['latitude', 'longitude', 'height']

class PerevalUpdateSerializer(serializers.ModelSerializer):
    coords = PerevalCoordsUpdateSerializer()
    images = PerevalImageSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
            'level_winter', 'level_summer', 'level_autumn', 'level_spring',
            'status', 'coords', 'images'
        ]

    def update(self, instance, validated_data):
        # Извлекаем вложенные данные
        coords_data = validated_data.pop('coords', None)
        images_data = validated_data.pop('images', None)

        # Обновление простых полей
        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.add_time = validated_data.get('add_time', instance.add_time)
        instance.level_winter = validated_data.get('level_winter', instance.level_winter)
        instance.level_summer = validated_data.get('level_summer', instance.level_summer)
        instance.level_autumn = validated_data.get('level_autumn', instance.level_autumn)
        instance.level_spring = validated_data.get('level_spring', instance.level_spring)
        instance.save()

        # Обновление координат
        if coords_data:
            coords_serializer = PerevalCoordsUpdateSerializer(instance.coords, data=coords_data, partial=True)
            if coords_serializer.is_valid(raise_exception=True):
                coords_serializer.save()

        # Обновление изображений: удалить старые и добавить новые
        if images_data:
            instance.images.all().delete()
            for img in images_data:
                PerevalImage.objects.create(pereval=instance, **img)

        return instance
