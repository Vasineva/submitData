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
        fields = ['title', 'image_url']


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




