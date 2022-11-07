from decimal import Decimal
from django.test import TestCase
from products.models import Product
from products.factories import ProductFactory


class ProductModelTests(TestCase):
    """Test models."""

    def setUp(self):
        self.productobj = ProductFactory()

    def test_create_product(self):
        """Test creating a product is successful."""

        product = Product.objects.create(
            name="Sample recipe name",
            is_available=True,
            on_promo=False,
            price=Decimal("5.50"),
            description="Sample receipe description.",
        )
        self.assertEqual(str(product), product.name)
