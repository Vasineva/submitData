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
        fields = ['id', 'title', 'image_url', 'pereval']


class PerevalAddedSerializer(serializers.ModelSerializer):
    coords = PerevalCoordsSerializer()
    level_winter = serializers.CharField(max_length=3, required=False, allow_blank=True)
    level_summer = serializers.CharField(max_length=3, required=False, allow_blank=True)
    level_autumn = serializers.CharField(max_length=3, required=False, allow_blank=True)
    level_spring = serializers.CharField(max_length=3, required=False, allow_blank=True)
    user_email = serializers.EmailField(write_only=True)
    user = serializers.HiddenField(default=None)

    class Meta:
        model = PerevalAdded
        exclude = []

    def create(self, validated_data):
        email = validated_data.pop('user_email')
        try:
            user = PerevalUser.objects.get(email=email)
        except PerevalUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не зарегистрирован.")

        coords_data = validated_data.pop('coords')
        coords = PerevalCoords.objects.create(**coords_data)

        validated_data['user'] = user
        validated_data['coords'] = coords
        return PerevalAdded.objects.create(**validated_data)




