from django_filters import rest_framework as filters
from ..models import Product
import django_filters


class ProductFilterset(filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["name"]
