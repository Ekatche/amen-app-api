"""
Serializer for inventory APIs
"""
from rest_framework import serializers
from ..models import Inventory
from products.serializers import ProductSerializer


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "quantity_sold",
            "total",
            "date_created",
            "date_updated",
        ]
