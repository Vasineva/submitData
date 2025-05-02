
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PerevalAddedSerializer, PerevalInfoSerializer, PerevalUpdateSerializer
from .models import PerevalAdded
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SubmitData(APIView):
    # Описание GET-запроса для получения перевалов по email
    @swagger_auto_schema(
        operation_description="Получить список перевалов по email пользователя",
        manual_parameters=[
            openapi.Parameter(
                'user__email',
                openapi.IN_QUERY,
                description="Email пользователя, чьи перевалы нужно получить",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: PerevalInfoSerializer(many=True)}
    )

    def get(self, request):
        # Получаем перевалы, связанные с этим email
        email = request.query_params.get('user__email')
        if not email:
            return Response({'error': 'Не указан параметр user__email'}, status=400)

        perevals = PerevalAdded.objects.filter(user__email=email)
        serializer = PerevalInfoSerializer(perevals, many=True)
        return Response(serializer.data, status=200)

    # Описание POST-запроса на добавление перевала
    @swagger_auto_schema(
        operation_description="Отправить новый перевал",
        request_body=PerevalAddedSerializer,
        responses={201: openapi.Response(description="Успешное создание", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                'message': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))}
    )

    def post(self, request):
        # Добавление перевала в БД
        serializer = PerevalAddedSerializer(data=request.data)
        if serializer.is_valid():
            return self.handle_valid_data(serializer)
        return self.handle_invalid_data(serializer)

    def handle_valid_data(self, serializer):
        try:
            # Сохранение перевала, если данные валидны
            pereval = serializer.save()
            return Response({
                'status': 200,
                'message': None,
                'id': pereval.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'status': 500,
                'message': f'Ошибка при сохранении: {str(e)}',
                'id': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_invalid_data(self, serializer):
        # Возвращаем ошибку, если данные невалидны
        return Response({
            'status': 400,
            'message': 'Ошибка валидации',
            'errors': serializer.errors,
            'id': None
        }, status=status.HTTP_400_BAD_REQUEST)

class PerevalRetrieveUpdateView(APIView):
    def get(self, request, id):
        pereval = get_object_or_404(PerevalAdded, id=id)
        serializer = PerevalInfoSerializer(pereval)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        pereval = get_object_or_404(PerevalAdded, id=id)

        if pereval.status != 'new':
            return Response({
                'state': 0,
                'message': 'Запись не может быть отредактирована, так как ее статус не "new".'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = PerevalUpdateSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'state': 1}, status=status.HTTP_200_OK)
        return Response({'state': 0, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

