"""
Views for promotion app
"""

from core.permissions import ReadOnlyPermission
from rest_framework import viewsets, mixins

from ..models import Promotion, Coupons
from ..serializers import PromotionSerializer, CouponsSerializer


class CouponsView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    API end point to allow coupons to be viewed or listed
    """

    serializer_class = CouponsSerializer
    permission_classes = [ReadOnlyPermission]
    queryset = Coupons.objects.all()


class ProductPromotionView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    API end point to allow coupons to be viewed or listed
    """

    serializer_class = PromotionSerializer
    permission_classes = [ReadOnlyPermission]
    queryset = Promotion.objects.all()
