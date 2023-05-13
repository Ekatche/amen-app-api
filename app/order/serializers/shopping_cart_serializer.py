from rest_framework import serializers
from ..models import ShoppingCart, CartItem, WishList
from user.serializers import UserSerializer
from products.serializers import ProductSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = [
            "id",
            "customer",
            "date_created",
            "date_updated",
        ]


class WishListSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = ["id", "customer", "product", "date_created", "date_updated"]


class CartItemSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True)
    cart = ShoppingCartSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "products",
            "quantity",
            "date_created",
            "date_updated",
        ]
