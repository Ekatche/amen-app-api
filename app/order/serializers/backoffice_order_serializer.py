from ..models import Order, OrderItem
from rest_framework import serializers
from user.serializers import UserSerializer, ShippingAddressSerializer
from products.serializers import BackofficeProductSerializer


class OrderBakcofficeSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    shipping = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

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
    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related("customer", "shipping")
        return queryset

    def create(self, validated_data):
        """
        Create and return a new `Order` instance, given the validated data.
        """
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Order` instance, given the validated data.
        """
        return super().update(instance, validated_data)


class OrderItemBackofficeSerializer(serializers.ModelSerializer):
    order = OrderBakcofficeSerializer()
    product = BackofficeProductSerializer()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "order",
            "quantity",
            "date_created",
            "date_updated",
        ]

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related("order", "product")
        return queryset

    def create(self, validated_data):
        """
        Create and return a new `Order Item` instance, given the validated data.
        """
        return OrderItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Order Item` instance, given the validated data.
        """
        return super().update(instance, validated_data)
