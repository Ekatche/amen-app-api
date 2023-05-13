from factory.django import DjangoModelFactory
from ..models import Inventory
from products.factories import ProductFactory
import factory


class InventoryFactory(DjangoModelFactory):
    class Meta:
        model = Inventory

    product = factory.SubFactory(ProductFactory)
    quantity_sold = factory.Faker("pyint", min_value=1, max_value=50)
    total_produced = factory.Faker("pyint", min_value=50, max_value=100)
