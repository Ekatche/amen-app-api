from factory.django import DjangoModelFactory
from ..models import Inventory


class InventoryFactory(DjangoModelFactory):
    class Meta:
        model = Inventory

    quantity_sold = 5
    total = 10
