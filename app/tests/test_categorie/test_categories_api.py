from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.factories import UserAdminFactory
from categories.factories import CategoryFactory, SubCategoryFactory
from categories.models import Category, SubCategory
from categories.serializers import CategorySerializer, SubCategorySerializer

CATEGORY_URLS = reverse("category:category-list")
SUBCATEGORY_URLS = reverse("category:subcategory-list")


class PublicCategoriesAPITests(TestCase):
    """
    Test unauthenticated APi requests
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_permissions_needed_categories(self):
        """Test auth required to call api"""
        res = self.client.get(CATEGORY_URLS)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateCategoriesAPITests(TestCase):
    """
    Test authenticated APi requests
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = UserAdminFactory()
        self.client.force_authenticate(self.user)
        self.cat1 = CategoryFactory(slug="gaga")
        self.cat2 = CategoryFactory(slug="BOBO")
        SubCategoryFactory(category=self.cat1)
        SubCategoryFactory(category=self.cat2)

    def test_retrieve_categories(self):
        res = self.client.get(CATEGORY_URLS)

        categories = Category.objects.all().order_by("id")
        serializer = CategorySerializer(categories, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_subcategories(self):
        res = self.client.get(SUBCATEGORY_URLS)
        subcategories = SubCategory.objects.all().order_by("id")
        serializer = SubCategorySerializer(subcategories, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
