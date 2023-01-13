"""
Views for the producs API
"""

from core.permissions import ReadOnlyPermission
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from documents import ProductDocument
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from ..models import Product
from ..serializers import ProductSerializer, ProductSearchSerializer
from ..filtersets import ProductFilterset
from django_filters import rest_framework as filters


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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilterset

    def retrieve(self, request, id=None, category_name=None, sub_category=None):
        """
        API to retrieve product based on category
        or subcategory or id
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
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define filter fields
    filter_fields = {
        "id": {
            "field": "id",
            # Note, that we limit the lookups of id field in this example,
            # to `range`, `in`, `gt`, `gte`, `lt` and `lte` filters.
            "lookups": [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        "name": {
            "field": "name",
            "lookups": [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }
    # Define ordering fields
    ordering_fields = {"id": "id", "name": "name"}
