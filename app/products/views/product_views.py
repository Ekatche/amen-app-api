"""
Views for the producs API
"""

from rest_framework import viewsets
from ..models import Product
from ..serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """View for manage Product APIs"""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = []
    permission_classes = []
