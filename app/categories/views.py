from rest_framework import viewsets
from .models import SubCategory, Category
from .serializers import CategorySerializer, SubCategorySerializer
from core.permissions import BackofficePermission


class CategoryViewset(viewsets.ModelViewSet):
    """
    API end point to allow category to be viewed or edited
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [BackofficePermission]


class SubCategoryViewset(viewsets.ModelViewSet):
    """
    API end point to allow Subcategory to be viewed ar edited
    """

    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [BackofficePermission]
