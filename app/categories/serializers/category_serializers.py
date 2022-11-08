from rest_framework import serializers
from ..models import SubCategory, Category


class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "is_active", "date_created", "date_updated"]


class SubCategorySerializer(serializers.Serializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = ["id", "name", "category", "date_created", "date_updated"]
