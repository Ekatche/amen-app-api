from core.permissions import BackofficePermission
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from ..models import Order, OrderItem
from ..serializers import OrderBakcofficeSerializer, OrderItemBackofficeSerializer


class OrderItemBackofficeViewSet(viewsets.ModelViewSet):
    """
    APi that allow order items to be viewed or edited
    allow only admin user to modify shopping cart
    """

    authentication_classes = ()
    permission_classes = [BackofficePermission]
    serializer_class = OrderItemBackofficeSerializer

    def get_queryset(self):
        queryset = OrderItem.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)


class OrderBackofficeViewset(viewsets.ModelViewSet):
    """
    API endpoint to allow order to be viewed and created
    """

    authentication_classes = ()
    permission_classes = [BackofficePermission]
    serializer_class = OrderBakcofficeSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)
