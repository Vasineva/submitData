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
       class Meta:
           model = PerevalImage
           fields = ['title', 'image_url']

class PerevalAddedSerializer(serializers.ModelSerializer):
   class Meta:
       user = PerevalUserSerializer()
       coords = PerevalCoordsSerializer()
       images = PerevalImageSerializer(many=True, write_only=True) #many=True список изображений
       # Уровни сложности по сезонам передаются как словарь
       level = serializers.DictField(child=serializers.CharField(), write_only=True)

       class Meta:
           model = PerevalAdded
           fields = [
               'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
               'user', 'coords', 'level', 'images'
           ]  # Поля, которые участвуют в сериализации