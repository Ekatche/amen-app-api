from categories.models import Category, SubCategory
from django.test import TestCase


class CategoryModelTests(TestCase):
    """Test models."""

    def test_create_category(self):
        """Test creating a recipe is successful."""

        category = Category.objects.create(name="Sample recipe name", is_active=True)

        self.assertEqual(str(category), category.name)

    def test_create_subcategory(self):
        category = Category.objects.create(name="Sample category", is_active=True)
        sub_category = SubCategory.objects.create(
            name="Sample subcategory",
            category=category,
        )

        self.assertEqual(str(sub_category), sub_category.name)
