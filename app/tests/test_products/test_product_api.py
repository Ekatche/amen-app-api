"""
Test for products API
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.factories import UserAdminFactory
from products.models import Product
from categories.models import Category
from products.factories import (
    ProductFactory,
)
from categories.factories import SubCategoryFactory, CategoryFactory

# from products.serializers import ProductSerializer


PRODUCTS_URL = reverse("product:product-list")


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


def create_product(**params):
    """Create and return a sample product"""
    defaults = {
        "name": "Test product",
        "description": "Sample Descritpion",
        "price": Decimal("5.25"),
        "is_available": True,
        "on_promo": False,
    }
    defaults.update(params)

    product = Product.objects.create(**defaults)
    return product


class PublicProductAPITest(TestCase):
    """Test Unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Test category", is_active=True)

    def test_auth_required(self):
        """Test unauthenticated user can access products"""

        create_product()

        res = self.client.get(PRODUCTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # products = Product.objects.all().order_by("id")
        # serializer = ProductSerializer(products, many=True)
        # self.assertEqual(res.data, serializer.data)


class PrivateProductApiTest(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = UserAdminFactory()
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test retrieving a list of product"""

        create_product()
        create_product()

        res = self.client.get(PRODUCTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # products = Product.objects.all().order_by("id")
        # serializer = ProductSerializer(products, many=True)
        # self.assertEqual(res.data, serializer.data)

    def test_retrieve_product_by_sub_category(self):
        subcategory = SubCategoryFactory()
        product = ProductFactory(subcategory=subcategory)
        link = f"/api/product/?subcategory_name={product.subcategory.name}"
        res = self.client.get(link)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"][0]["name"], product.name)

    def test_retrieve_product_by_category(self):
        category = CategoryFactory(name="test_VTF")
        product = ProductFactory(categories=(category,))
        link = f"/api/product/?category_name={category.name}"
        res = self.client.get(link)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"][0]["name"], product.name)
