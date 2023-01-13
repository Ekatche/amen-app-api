from core.permissions import ReadOnlyPermission, BackofficePermission
from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as filters
from .filtersets import (
CategoryFilter,
SubCategoryFilter,
)
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
    """
    API end point to manage category
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (BackofficePermission,)
    serializer_class = CategoryBackofficeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CategoryFilter
    queryset = Category.objects.all()

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
    permission_classes = [
        ReadOnlyPermission,
    ]


class SubCategoryBackofficeViewset(viewsets.ModelViewSet):
    """
    API end point to manage subcategory
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (BackofficePermission,)
    serializer_class = SubCategoryBackofficeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubCategoryFilter

    def get_queryset(self):
        queryset = SubCategory.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)
