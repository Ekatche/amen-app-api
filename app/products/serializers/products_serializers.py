"""
Serializers for products APIs
"""

from rest_framework import serializers
from ..models import Product
from categories.serializers import CategorySerializer, SubCategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    subcategory = SubCategorySerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "slug",
            "category",
            "subcategory",
            "description",
            "is_available",
            "on_promo",
            "promo",
        ]
        lookup_field = "slug"
        read_only_fields = ["id"]
        extra_kwargs = {"url": {"lookup_field": "slug"}}
