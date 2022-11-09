"""
Serializers for products APIs
"""

from rest_framework import serializers
from ..models import Product
from inventory.serializers import InventorySerializer
from categories.serializers import CategorySerializer, SubCategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    inventory = InventorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "slug",
            "inventory",
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
