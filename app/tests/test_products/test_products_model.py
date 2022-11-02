from decimal import Decimal
from django.test import TestCase
from products.models import Product
from categories.models import Category


class ProductModelTests(TestCase):
    """Test models."""

    def test_create_product(self):
        """Test creating a recipe is successful."""

        product = Product.objects.create(
            name='Sample recipe name',
            is_available=True,
            on_promo=False,
            price=Decimal('5.50'),
            description='Sample receipe description.',
        )
        self.assertEqual(str(product), product.name)
