"""
Serializers for products APIs
"""

from rest_framework import serializers
from ..models import Product, Coupons, Promotion
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from documents import ProductDocument
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
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
    coupons = CouponsSerializer()

    class Meta:
        model = Promotion
        fields = [
            "id",
            "name",
            "period",
            "coupons",
            "is_active",
            "is_schedule",
            "date_start",
            "date_end",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    subcategory = SubCategorySerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)
    promotion = PromotionSerializer(source="promo", read_only=True)
    image = MediaSerializer(source="images", read_only=True, many=True)
    product_inventory = InventorySerializer(source="inventory", read_only=True)
    promo_price = serializers.SerializerMethodField()

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
            "promotion",
            "promo_price",
        ]
        lookup_field = "slug"
        read_only_fields = ["id"]
        extra_kwargs = {"url": {"lookup_field": "slug"}}

    def get_promo_price(self, obj):
        prod = Product.objects.get(id=obj.id)
        if prod.on_promo:
            try:
                product = Product.objects.get(
                    Q(promo__is_active=True)
                    & Q(promo__coupons__is_active=True)
                    & Q(id=obj.id)
                )
                return product.promo_price
            except ObjectDoesNotExist:
                return None
        else:
            return prod.promo_price


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
            "promo_price",
        ]
