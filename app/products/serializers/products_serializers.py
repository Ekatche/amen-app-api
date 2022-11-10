"""
Serializers for products APIs
"""

from rest_framework import serializers
from ..models import Product, Coupons, Promotion, Media
from categories.serializers import CategorySerializer, SubCategorySerializer


class CouponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupons
        fields = [
            "id",
            "name",
            "code",
            "discount",
            "is_active",
            "date_updated",
            "date_created",
        ]


class PromotionSerializer(serializers.ModelSerializer):
    coupons = CouponsSerializer(read_only=True)

    class Meta:
        model = Promotion
        fields = [
            "id",
            "name",
            "period",
            "coupons",
            "date_start",
            "date_end" "date_updated",
            "date_created",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    subcategory = SubCategorySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    promo = PromotionSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "slug",
            "images",
            "category",
            "subcategory",
            "description",
            "is_available",
            "on_promo",
            "promo",
        ]
        lookup_field = "slug"
        read_only_fields = ["id"]
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class MediaSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Media
        fields = ["__all__"]
