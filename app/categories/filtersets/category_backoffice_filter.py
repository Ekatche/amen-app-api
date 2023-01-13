from django_filters import rest_framework as filters
from ..models import SubCategory, Category
import django_filters

class CategoryFilter(filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = Category
        fields = ['name']


class SubCategoryFilter(filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = SubCategory
        fields = ['name']
