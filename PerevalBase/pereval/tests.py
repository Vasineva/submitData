from django.test import TestCase
from rest_framework.test import APIClient
from .models import *
from rest_framework import status


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

    def test_create_and_get_pereval(self):
        # POST запрос для создания перевала с новым пользователем
        response = self.client.post('/api/submitData/', self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 200)  # Выводим статус 200, если создано успешно
        pereval_id = response.data['id']

        # Проверка, что новый пользователь был добавлен в базу данных
        user_email = self.valid_data['user']['email']
        user = PerevalUser.objects.get(email=user_email)
        self.assertIsNotNone(user)

        # GET запрос по ID
        get_response = self.client.get(f'/api/submitData/{pereval_id}/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['title'], self.valid_data['title'])
        self.assertEqual(get_response.data['user']['email'], self.valid_data['user']['email'])


