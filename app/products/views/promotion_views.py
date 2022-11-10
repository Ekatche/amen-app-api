"""
Views for promotion app
"""

from rest_framework import viewsets
from core.permissions import ReadOnlyPermission
from ..models import Promotion, Coupons
from ..serializers import PromotionSerializer, CouponsSerializer


class CouponsViewset(viewsets.ModelViewSet):
    """
    API end point to manage coupons
    """

    serializer_class = CouponsSerializer
    permission_classes = [ReadOnlyPermission]
    queryset = Coupons.objects.all()


class ProductPromotionView(viewsets.ModelViewSet):
    """
    View for manage promotion APIs
    """

    serializer_class = PromotionSerializer
    permission_classes = [ReadOnlyPermission]
    queryset = Promotion.objects.all()
