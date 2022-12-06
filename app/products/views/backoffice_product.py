from core.permissions import BackofficePermission
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from ..serializers import BackofficeProductSerializer
from ..models import Product


class BackofficeProductViewset(viewsets.ModelViewSet):
    """
    API for admin to manage products
    Admin user must be authenticated and have specific authorizations to perform tasks
    """

    authentication_classes = ()
    permission_classes = [BackofficePermission]
    serializer_class = BackofficeProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)
