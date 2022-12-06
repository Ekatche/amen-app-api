"""
URL mapping for the order app
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewset,
    ShoppingcartViewset,
    OrderBackofficeViewset,
    OrderItemBackofficeViewSet,
    CartItemViewSet,
    OrderItemViewSet,
)

router = DefaultRouter()
router.register("order", OrderViewset, basename="order")
router.register("order-items", OrderItemViewSet, basename="order-items")
router.register("shoppingcart", ShoppingcartViewset, basename="shoppingcart")
router.register("shoppingcart-items", CartItemViewSet, basename="shoppingcart-items")
router.register("backoffice/order", OrderBackofficeViewset, basename="backoffice-order")
router.register(
    "backoffice/order-items",
    OrderItemBackofficeViewSet,
    basename="backoffice-order-items",
)

app_name = "order"

urlpatterns = [
    path("", include(router.urls)),
]
