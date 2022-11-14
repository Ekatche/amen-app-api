from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.factories import UserAdminFactory

# from inventory.models import Inventory
# from inventory.serializers import InventorySerializer
from inventory.factories import InventoryFactory

INVENTORY_URLS = reverse("inventory:inventory-list")


class PublicInventoryAPITests(TestCase):
    """
    Test unauthenticated API requests
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_permission_needed_(self):
        res = self.client.get(INVENTORY_URLS)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PivrateInventoryAPITests(TestCase):
    """
    Test authenticated API requests
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = UserAdminFactory()
        self.client.force_authenticate(self.user)

    def test_retrieving_inventory(self):
        InventoryFactory()
        InventoryFactory()

        res = self.client.get(INVENTORY_URLS)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # inventory = Inventory.objects.all().order_by("id")
        # serializer = InventorySerializer(inventory, many=True)
        # self.assertEqual(res.data, serializer.data)
