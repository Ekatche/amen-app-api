import re

import django_filters
from django.db.models import Q
from django.db.models.functions import Lower
from django_filters import rest_framework as filters

from ..models import Order


class OrderFilterset(filters.FilterSet):
    term = django_filters.CharFilter(method="search")

    class meta:
        model = Order
        fields = ["term"]

    def search(self, queryset, name, value):
        list_term = re.sub(" +", " ", value).split(" ")
        queryset = queryset.annotate(lower_first_name=Lower("customer__first_name"))
        queryset = queryset.annotate(lower_last_name=Lower("customer__last_name"))
        list_Q = []
        for term in list_term:
            list_Q.append(Q(lower_first_name__contains=term))
            list_Q.append(Q(lower_last_name__contains=term))
            list_Q.append(Q(id=term))

        query = list_Q.pop()
        for q in list_Q:
            query |= q

        return queryset.filter(query)
