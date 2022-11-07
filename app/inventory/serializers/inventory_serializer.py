"""
Serializer for inventory APIs
"""
from rest_framework import serializers
from ..models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "quantity_sold" "total",
            "date_created",
            "date_updated",
        ]
