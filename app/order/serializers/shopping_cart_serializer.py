from rest_framework import serializers
from ..models import ShoppingCart
from user.serializers import UserSerializer
from products.serializers import ProductSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    products = ProductSerializer(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = [
            "id",
            "products",
            "order" "customer",
            "quantity",
            "amount_due",
            "date_created",
            "date_updated",
        ]
