"""
Test for products API
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


from products.models import Product
from categories.models import Category
from products.serializers import ProductSerializer


PRODUCTS_URL =reverse("product:product-list")

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)

def create_product(**params):
    """ Create and return a sample product """
    defaults = {
        'name': 'Test product',
        'description': 'Sample Descritpion',
        'price': Decimal('5.25'),
        'is_available': True,
        'on_promo': False,
    }
    defaults.update(params)

    product = Product.objects.create(**defaults)
    return product


class PublicProductAPITest(TestCase):
    """ Test Unauthenticated API requests """
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Test category",
            is_active=True
        )

    def test_auth_required(self):
        """ Test un authenticated user can access products"""

        create_product()

        res = self.client.get(PRODUCTS_URL)
        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateProductApiTest(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="test@example.com",
            password="Testpass123",
            first_name="Test",
            last_name="Name",
        )
        self.client.force_authenticate(self.user)
        self.category = Category.objects.create(
            name="Test category",
            is_active=True
        )

    def test_retrieve_products(self):
        """ Test retrieving a list of product """

        create_product()

        res = self.client.get(PRODUCTS_URL)
        products = Product.objects.all().order_by('id')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
