"""
Views for the producs API
"""

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from ..models import Product
from ..serializers import ProductSerializer, ProductSearchSerializer
from core.permissions import ReadOnlyPermission
from documents import ProductDocument
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

# from elasticsearch_dsl import Q


class ProductViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """
    API to manage products
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_available=True)
    lookup_field = "id"
    permission_classes = [ReadOnlyPermission]

    def retrieve(self, request, id=None, category_name=None, sub_category=None):
        """
        API to retrieve product based on category
        or subcategory
        """
        if category_name:
            queryset = Product.objects.filter(is_available=True).filter(
                category__name=category_name
            )
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif sub_category:
            queryset = Product.objects.filter(sub_category__name=sub_category)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif id:
            queryset = Product.objects.filter(id=id)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
        )


class SearchProductView(BaseDocumentViewSet):
    serializer_class = ProductSearchSerializer
    document = ProductDocument
    pagination_class = PageNumberPagination
    lookup_field = "id"
    search_fields = ("name",)
