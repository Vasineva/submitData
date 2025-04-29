from django.urls import path
from .views import SubmitData, PerevalRetrieveUpdateView

urlpatterns = [
    path('submitData/', SubmitData.as_view(), name='submit_data'),
    path('submitData/<int:id>/', PerevalRetrieveUpdateView.as_view(), name='submit_data_detail'),
]