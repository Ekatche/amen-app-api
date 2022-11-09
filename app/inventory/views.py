from rest_framework import viewsets
from .models import Inventory
from .serializers import InventorySerializer
from core.permissions import BackofficePermission


class InventoryViewSet(viewsets.ModelViewSet):
    """
    API end point to allow Inventory to be viewed or edited
    """

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [BackofficePermission]
