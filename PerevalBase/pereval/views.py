
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PerevalAddedSerializer, PerevalInfoSerializer, PerevalUpdateSerializer
from .models import PerevalAdded
from django.shortcuts import get_object_or_404


class SubmitData(APIView):
    def post(self, request):
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