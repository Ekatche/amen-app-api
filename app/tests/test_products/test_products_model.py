from decimal import Decimal
from django.test import TestCase
from products.models import Product
from model_bakery import baker


class ProductModelTests(TestCase):
    """Test models."""

    def setUp(self):
        self.productobj = baker.make(
            Product, name="Test Obj1", category__name="Test Cat1"
        )

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

    def test_create_product_and_category(self):
        """Test creating a product and assign a category"""

        product = Product.objects.prefetch_related("catgory").values(
            "name", "category__name"
        )

        self.assertEqual(product[0].get("name"), "Test Obj1")
        self.assertEqual(product[0].get("category__name"), "Test Cat1")
