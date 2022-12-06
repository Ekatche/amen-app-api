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
    CouponsView,
    SearchProductView,
    BackofficeProductViewset,
    BackofficeCouponsViewset,
    BackofficePromotionViewset
)

router = DefaultRouter()
router.register("product", ProductViewSet)
router.register("coupons", CouponsView)
router.register("promotion", ProductPromotionView)
router.register("search", SearchProductView, basename="search-product")
router.register(
    "backoffice/product", BackofficeProductViewset, basename="backoffice-product"
)
router.register(
    "backoffice/coupons", BackofficeCouponsViewset, basename="backoffice-coupons"
)
router.register(
    "backoffice/promotions", BackofficePromotionViewset, basename="backoffice-promotions"
)
app_name = "product"

urlpatterns = [
    path("", include(router.urls)),
]
