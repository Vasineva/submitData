from .models import PerevalUser, PerevalCoords, PerevalAdded, PerevalImage
from django.db import transaction


class PerevalDatabase:
    @staticmethod
    @transaction.atomic
    def create_pereval(data):
        user_data = data.pop('user')
        coords_data = data.pop('coords')
        images_data = data.pop('images')

        user, created = PerevalUser.objects.get_or_create(email=user_data['email'], defaults=user_data)

        coords = PerevalCoords.objects.create(**coords_data)

        pereval = PerevalAdded.objects.create(user=user, coords=coords, **data)

        for img in images_data:
            PerevalImage.objects.create(pereval=pereval, title=img['title'], image_url=img['image_url'])

        return pereval