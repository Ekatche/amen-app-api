from rest_framework import serializers

from ..models import SubCategory, Category


class CategoryBackofficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "is_active"]

    def create(self, validated_data):
        """
        Create and return a new `Category` instance, given the validated data.
        """
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Category` instance, given the validated data.
        """
        return super().update(instance, validated_data)


class SubCategoryBackofficeSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = SubCategory
        fields = ["id", "name", "category"]

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related("category")
        return queryset

    def create(self, validated_data):
        """
        Create and return a new `Subcategory` instance, given the validated data.
        """
        return SubCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Subcategory` instance, given the validated data.
        """
        return super().update(instance, validated_data)
