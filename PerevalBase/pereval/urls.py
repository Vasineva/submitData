from django.urls import path
from .views import SubmitData

urlpatterns = [
    path('submit_data/', SubmitData.as_view(), name='submit_data'),
]