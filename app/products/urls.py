"""
URL mapping for the product app
"""

from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    ProductPromotionView,
    CouponsViewset,
    SearchProductView,
)

router = DefaultRouter()
router.register("product", ProductViewSet)
router.register("coupons", CouponsViewset)
router.register("promotion", ProductPromotionView)
router.register("search", SearchProductView, basename="searchproduct")

app_name = "product"

urlpatterns = [
    path("", include(router.urls)),
]
