from rest_framework import viewsets, mixins
from .models import SubCategory, Category
from .serializers import CategorySerializer, SubCategorySerializer
from core.permissions import ReadOnlyPermission


class CategoryViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """
    API end point to allow category to be viewed or listed
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyPermission]


class SubCategoryViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """
    API end point to allow Subcategory to be viewed ar listed
    """

    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [ReadOnlyPermission]
