import django_filters
from .models import PerevalAdded

class PerevalAddedFilter(django_filters.FilterSet):
    user__email = django_filters.CharFilter(field_name='user__email', lookup_expr='iexact')

    class Meta:
        model = PerevalAdded
        fields = ['user__email']