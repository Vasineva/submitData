from .models import *
from rest_framework import serializers


class PerevalUserSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       pass


class PerevalCoordsSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       pass


class PerevalAddedSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       pass

class PerevalImageSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       pass