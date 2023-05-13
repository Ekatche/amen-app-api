"""
Serializer for inventory APIs
"""
from rest_framework import serializers
from ..models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    available_quantity = serializers.IntegerField(
        source="get_available_quatity", read_only=True
    )

    class Meta:
        model = Inventory
        fields = [
            "id",
            "quantity_sold",
            "total_produced",
            "available_quantity",
        ]

    def create(self, validated_data):
        """
        Create and return a new `Order Item` instance, given the validated data.
        """
        return Inventory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Order Item` instance, given the validated data.
        """
        return super().update(instance, validated_data)
