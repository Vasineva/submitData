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

class CoordsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalCoords
        fields = ['latitude', 'longitude', 'height']

class PerevalUpdateSerializer(serializers.ModelSerializer):
    coords = CoordsUpdateSerializer()
    images = PerevalImageSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
            'level_winter', 'level_summer', 'level_autumn', 'level_spring',
            'status', 'coords', 'images'
        ]

    def update(self, instance, validated_data):
        if instance.status != 'new':
            raise serializers.ValidationError("Могут быть обновлены только записи со статусом 'new'.")

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
        return instance
