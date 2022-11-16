"""
Serializers for products APIs
"""

from rest_framework import serializers
from ..models import Product, Coupons, Promotion
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from documents import ProductDocument
from .media_serializer import MediaSerializer
from categories.serializers import CategorySerializer, SubCategorySerializer
from inventory.serializers import InventorySerializer


class CouponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupons
        fields = [
            "id",
            "name",
            "code",
            "discount",
            "is_active",
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
            "date_end",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    subcategory = SubCategorySerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)
    promo = PromotionSerializer(read_only=True)
    image = MediaSerializer(source="images", read_only=True, many=True)
    product_inventory = InventorySerializer(source="inventory", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "slug",
            "image",
            "product_inventory",
            "categories",
            "subcategory",
            "description",
            "is_available",
            "on_promo",
            "promo",
        ]
        lookup_field = "slug"
        read_only_fields = ["id"]
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class ProductSearchSerializer(DocumentSerializer):
    class Meta:
        document = ProductDocument

        fields = [
            "id",
            "name",
            "price",
            "slug",
            "images",
            "inventory",
            "categories",
            "subcategory",
            "description",
            "is_available",
            "on_promo",
            "promo",
        ]
