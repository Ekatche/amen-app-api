from ..models import Order
from rest_framework import serializers
from user.serializers import UserSerializer
from .shopping_cart_serializer import ShoppingCartSerializer
from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    products = ProductSerializer(read_only=True)
    shoppingcart = ShoppingCartSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "shoppingcart" "customer",
            "products",
            "quantity",
            "amount_due",
            "date_created",
            "date_updated",
            "status",
            "reason",
        ]
