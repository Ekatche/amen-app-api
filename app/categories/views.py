from core.permissions import ReadOnlyPermission, BackofficePermission
from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied

from .models import SubCategory, Category
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    CategoryBackofficeSerializer,
    SubCategoryBackofficeSerializer,
)


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


class CategoryBackofficeViewset(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = [BackofficePermission]
    serializer_class = [CategoryBackofficeSerializer]

    def get_queryset(self):
        queryset = Category.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)


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


class SubCategoryBackofficeViewset(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = [BackofficePermission]
    serializer_class = [SubCategoryBackofficeSerializer]

    def get_queryset(self):
        queryset = SubCategory.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)
