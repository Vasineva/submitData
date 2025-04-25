
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PerevalAddedSerializer


class SubmitData(APIView):
    def post(self, request):
        # для сериализатора
        serializer = PerevalAddedSerializer(data=request.data)

        # валидность данных
        if serializer.is_valid():
            return self.handle_valid_data(serializer)

        # данные невалидны, возвращаем ошибку
        return self.handle_invalid_data(serializer)

    def handle_valid_data(self, serializer):
        # сохранение данных
        pass

    def handle_invalid_data(self, serializer):
        # обработка ошибкок
        pass