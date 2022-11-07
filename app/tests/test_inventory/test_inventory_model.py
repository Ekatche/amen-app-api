from django.test import TestCase
from inventory.models import Inventory
from inventory.factories import InventoryFactory
from products.models import Product
from products.factories import ProductFactory


class InventoryModelTest(TestCase):
    """
    test Inventory model
    """
    def setUp(self) -> None:
        self.product= ProductFactory(name= "test for inventory")
        InventoryFactory(product = self.product)

    def test_create_product_and_get_inventory(self):
        """Test creating a product inventory is successful"""
        product = Inventory.objects.get(product=Product.objects.get(name="test for inventory"))
        self.assertEqual(str(product.product.name), "test for inventory")
        self.assertEqual(product.total, 10)
