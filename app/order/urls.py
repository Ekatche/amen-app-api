"""
URL mapping for the order app
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from .views import OrderViewset, ShoppingcartViewset

router = DefaultRouter()
router.register("order", OrderViewset, basename="order")
router.register("shoppingcart", ShoppingcartViewset, basename="order")

app_name = "order"

urlpatterns = [
    path("", include(router.urls)),
]
