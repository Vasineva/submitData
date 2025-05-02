from django.test import TestCase
from rest_framework.test import APIClient
from .models import *


class PerevalAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем пользователя
        self.user = PerevalUser.objects.create(
            email='qwerty@mail.ru',
            fam='Пупкин',
            name='Василий',
            otc='Иванович',
            phone='+7 555 55 55'
        )

        self.valid_data = {
            "beauty_title": "пер.",
            "title": "Пхия",
            "other_titles": "Триев",
            "connect": "",
            "add_time": "2021-09-22 13:18:13",
            "user": {
                "email": "qwerty@mail.ru",
                "fam": "Пупкин",
                "name": "Василий",
                "otc": "Иванович",
                "phone": "+7 555 55 55"
            },
            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200"
            },
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""
            },
            "images": [
                {"title": "Седловина", "image_url": "http://example.com/image1.jpg"},
                {"title": "Подъем", "image_url": "http://example.com/image2.jpg"}
            ]
        }


