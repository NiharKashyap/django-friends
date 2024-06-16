from django.contrib.auth.models import User
import django_filters
from django.db.models import Q

class UserFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_by_all_fields')

    class Meta:
        model = User
        fields = []

    def filter_by_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(email__iexact=value) |
            Q(username__icontains=value)
        )