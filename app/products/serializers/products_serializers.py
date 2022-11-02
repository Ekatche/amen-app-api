"""
Serializers for products APIs
"""

from rest_framework import serializers
from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    class Meta:
        model = Product
        fields = ["id", "name", "price", "category"]
        read_only_fields = ["id"]
