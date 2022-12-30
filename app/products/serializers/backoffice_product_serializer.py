from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import serializers

# from .media_serializer import MediaSerializer
# from ..serializers import PromotionSerializer
from ..models import Product, Coupons, Promotion


class CouponsBackofficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupons
        fields = [
            "id",
            "name",
            "code",
            "discount",
            "is_active",
        ]

    def create(self, validated_data):
        return Coupons.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PromotionBackofficeSerializer(serializers.ModelSerializer):
    # coupons = CouponsBackofficeSerializer()

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

    def create(self, validated_data):
        return Promotion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related("coupons")
        return queryset


def get_promo_price(obj):
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


class BackofficeProductSerializer(serializers.ModelSerializer):
    # subcategory = SubCategorySerializer(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # promotion = PromotionSerializer(source="promo", allow_null=True, read_only=True)
    # images = MediaSerializer(many=True, read_only=True, )
    # inventory = InventorySerializer(read_only=True)
    promotion = serializers.CharField(source="promo", allow_null=True)
    promo_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "slug",
            "inventory",
            "categories",
            "subcategory",
            "description",
            "is_available",
            "on_promo",
            "promotion",
            "promo_price",
        ]

    @staticmethod
    def get_promo_price(obj):
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
        queryset = queryset.prefetch_related("images", "inventory")
        return queryset

    def create(self, validated_data):
        """
        Create and return a new `Product` instance, given the validated data.
        """
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `OrderItem` instance, given the validated data.
        """
        return super().update(instance, validated_data)
