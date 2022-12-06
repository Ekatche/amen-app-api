from categories.serializers import CategorySerializer, SubCategorySerializer
from inventory.serializers import InventorySerializer
from rest_framework import serializers
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from .media_serializer import MediaSerializer
from ..models import Product
from ..serializers import PromotionSerializer


class BackofficeProductSerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer()
    categories = CategorySerializer(many=True)
    promotion = PromotionSerializer(source="promo")
    image = MediaSerializer(source="images", many=True)
    product_inventory = InventorySerializer(source="inventory")
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
    @staticmethod
    def setup_eager_loading(queryset):
        return queryset

    def create(self, validated_data):
        """
        Create and return a new `Product` instance, given the validated data.
        """
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
       Update and return an existing `Snippet` instance, given the validated data.
       """
        return super().update(instance, validated_data)
