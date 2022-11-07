import factory
from factory.django import DjangoModelFactory
from ..models import Inventory
from products.factories import ProductFactory


class InventoryFactory(DjangoModelFactory):
    class Meta:
        model = Inventory

    product = factory.SubFactory(ProductFactory)
    quantity_sold = 5
    total = 10
