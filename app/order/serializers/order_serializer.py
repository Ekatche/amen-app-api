from ..models import Order, OrderItem
from rest_framework import serializers
from user.serializers import UserSerializer, ShippingAddressSerializer
from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    shipping = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "shipping",
            "amount_due",
            "date_created",
            "date_updated",
            "status",
            "reason",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "order", "quantity", "date_created", "date_updated"]
