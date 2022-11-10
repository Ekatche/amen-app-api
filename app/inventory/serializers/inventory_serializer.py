"""
Serializer for inventory APIs
"""
from rest_framework import serializers
from ..models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    available_quantity = serializers.IntegerField(source="get_available_quatity")
    product_id = serializers.Field(source="product")

    class Meta:
        model = Inventory
        fields = [
            "id",
            "quantity_sold",
            "product_id",
            "total",
            "available_quantity",
            "date_created",
            "date_updated",
        ]
