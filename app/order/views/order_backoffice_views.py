from core.permissions import BackofficePermission
from django.db.models import Q
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..filtersets import OrderFilterset
from ..models import Order, OrderItem
from ..serializers import OrderBakcofficeSerializer, OrderItemBackofficeSerializer


class OrderItemBackofficeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    APi that allow order items to be viewed or edited
    allow only admin user to modify shopping cart
    """

    # authentication_classes = (JWTAuthentication,)
    # permission_classes = [BackofficePermission]
    serializer_class = OrderItemBackofficeSerializer

    def get_queryset(self):
        queryset = OrderItem.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        retrieve either with orderItem id or order_id
        """
        order_item_id = self.kwargs['id']
        try:
            queryset = self.get_queryset()
            order_items = queryset.filter(Q(id=order_item_id) | Q(order=order_item_id))
            if order_items:
                data = self.serializer_class(order_items, many=True).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({"Error": "The object does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)


class OrderBackofficeViewset(viewsets.ModelViewSet):
    """
    API endpoint to allow order to be viewed and created
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = [BackofficePermission]
    serializer_class = OrderBakcofficeSerializer
    filterset_class = OrderFilterset

    def get_queryset(self):
        queryset = Order.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)
