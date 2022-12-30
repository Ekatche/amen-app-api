from core.permissions import BackofficePermission
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Promotion, Coupons
from ..serializers import CouponsBackofficeSerializer, PromotionBackofficeSerializer


class BackofficePromotionViewset(viewsets.ModelViewSet):
    """
    API end point for backoffice coupons Management
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (BackofficePermission,)
    serializer_class = PromotionBackofficeSerializer

    def get_queryset(self):
        queryset = Promotion.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)


class BackofficeCouponsViewset(viewsets.ModelViewSet):
    """
    API end point for backoffice coupons Management
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (BackofficePermission,)
    serializer_class = CouponsBackofficeSerializer

    def get_queryset(self):
        queryset = Coupons.objects.all()
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)
