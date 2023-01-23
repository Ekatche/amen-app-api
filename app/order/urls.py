"""
URL mapping for the order app
"""

from django.urls import (
    path,
    include,
re_path
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

order_item_list = OrderItemBackofficeViewSet.as_view({
    'get': 'list'
})

order_item_detail = OrderItemBackofficeViewSet.as_view({
    "get": "retrieve",
})

order_item_update = OrderItemBackofficeViewSet.as_view({
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

router = DefaultRouter()
router.register("order", OrderViewset, basename="order")
router.register("order-items", OrderItemViewSet, basename="order-items")
router.register("shoppingcart", ShoppingcartViewset, basename="shoppingcart")
router.register("shoppingcart-items", CartItemViewSet, basename="shoppingcart-items")
router.register("backoffice/order", OrderBackofficeViewset, basename="backoffice-order")
app_name = "order"

urlpatterns = [
    path("", include(router.urls)),
    path("backoffice/order-items/", order_item_list, name='order-item-list'),
    re_path("^backoffice/order-items/(?P<id>.+)/$", order_item_detail, name='order-detail'),
    path('backoffice/order-items/<int:id>', order_item_update, name='order-update'),
]
