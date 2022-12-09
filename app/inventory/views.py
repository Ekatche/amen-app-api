from rest_framework import viewsets
from .models import Inventory
from .serializers import InventorySerializer
from core.permissions import BackofficePermission
from rest_framework.exceptions import PermissionDenied


class InventoryBackofficeViewSet(viewsets.ModelViewSet):
    """
    API end point to allow Inventory to be viewed or edited \n
    Only for Backoffice users
    """

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [BackofficePermission]

    def destroy(self, request, *args, **kwargs):
        if request.user.amen_role != "Administrateur":
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)
