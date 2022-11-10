from rest_framework import serializers
from ..models import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            "id",
            "image",
            "is_feature",
        ]
        read_only = True
