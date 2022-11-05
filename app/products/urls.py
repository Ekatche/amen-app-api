"""
URL mapping for the product app
"""

from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductPromotionView

router = DefaultRouter()
router.register("product", ProductViewSet)

app_name = "product"

urlpatterns = [
    path("", include(router.urls)),
    path("promotion/coupon/", ProductPromotionView.as_view()),
]