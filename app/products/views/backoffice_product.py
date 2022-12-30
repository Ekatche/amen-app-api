from core.permissions import BackofficePermission
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from ..models import Product, Media
from ..serializers import BackofficeProductSerializer, MediaSerializer


class BackofficeProductViewset(viewsets.ModelViewSet):
    """
    API for admin to manage products
    Admin user must be authenticated and have specific authorizations to perform tasks
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = [
        BackofficePermission,
    ]
    serializer_class = BackofficeProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)


class BackofficeMediaViewset(viewsets.ModelViewSet):
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = [
        BackofficePermission,
    ]
    serializer_class = MediaSerializer

    def get_queryset(self):
        queryset = Media.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)
