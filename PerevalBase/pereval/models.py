"""
Модели для REST API проекта ФСТР (Федерация спортивного туризма России).

1. PerevalUser — модель пользователя. Идентификация осуществляется по уникальному email.
   Содержит ФИО и номер телефона.
2. PerevalCoords — модель координат перевала. Содержит широту, долготу и высоту.
3. PerevalImage — модель изображения перевала. Хранит заголовок и URL изображения,
   связана с перевалом.
4. PerevalAdded — основная модель для хранения информации о перевале:
   - Названия, дата добавления, описание соединяемых точек.
   - Связь с пользователем, координатами, изображениями.
   - Уровни сложности по сезонам: зима, лето, осень, весна.
   - Статус модерации: новая, на проверке, принята или отклонена.

Уровни сложности и статусы задаются с помощью `choices`, что обеспечивает контроль вводимых
данных.
Модель PerevalImage связана с PerevalAdded через ForeignKey (один ко многим),
а координаты — через OneToOne (один к одному).
"""

from django.db import models
from django.utils import timezone


class PerevalUser(models.Model):
    email = models.EmailField()
    fam = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    otc = models.CharField(max_length=100, blank=True) # у пользователя может не быть отчества
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.fam} {self.name} ({self.email})"


class PerevalCoords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    def __str__(self):
        return f"Широта: {self.latitude}, Долгота: {self.longitude}, Высота: {self.height}"

class PerevalAdded(models.Model):
    beauty_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=255, blank=True)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField(default=timezone.now)
    level_winter = models.CharField(max_length=3, blank=True)
    level_summer = models.CharField(max_length=3, blank=True)
    level_autumn = models.CharField(max_length=3, blank=True)
    level_spring = models.CharField(max_length=3, blank=True)

    # Статус модерации
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('pending', 'На модерации'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    # Связи
    user = models.ForeignKey(PerevalUser, on_delete=models.CASCADE, related_name='perevals')
    coords = models.OneToOneField(PerevalCoords, on_delete=models.CASCADE, related_name='pereval')

    def __str__(self):
        return f"{self.beauty_title} {self.title} ({self.add_time.strftime('%Y-%m-%d')})"

class PerevalImage(models.Model):
    pereval = models.ForeignKey('PerevalAdded', on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=100)
    image_url = models.URLField()  # хранится ссылка на изображение

    def __str__(self):
        return f"{self.title} - {self.image_url}"


