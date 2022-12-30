from rest_framework import serializers
from ..models import Media


class MediaSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(use_url=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = [
            "id",
            "product",
            "image",
            "is_feature",
        ]

    def get_image(self, obj):
        return obj.image.url
