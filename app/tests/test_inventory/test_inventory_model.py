from django.test import TestCase
from inventory.models import Inventory
from products.models import Product
from decimal import Decimal


class InventoryModelTest(TestCase):
    """
    test Inventory model
    """

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name="Sample TEst 2",
            is_available=True,
            on_promo=False,
            price=Decimal("5.50"),
            description="Sample receipe description.",
        )
        Product.objects.create(
            name="Sample test 1",
            is_available=True,
            on_promo=False,
            price=Decimal("5.50"),
            description="Sample receipe description.",
        )
        Inventory.objects.create(
            product=Product.objects.get(id=1), total=100, quantity_sold=25
        )
        Inventory.objects.create(
            product=Product.objects.get(id=2), total=150, quantity_sold=75
        )

    def test_create_product_and_get_inventory(self):
        """Test creating a product inventory is successful"""
        product = Inventory.objects.get(product=Product.objects.get(id=1))
        self.assertEqual(str(product.product.name), "Sample TEst 2")
        self.assertEqual(product.total, 100)
