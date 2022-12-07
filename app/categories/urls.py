from django.urls import include, path
from rest_framework import routers
from .views import (
    SubCategoryViewset,
    CategoryViewset,
    CategoryBackofficeViewset,
    SubCategoryBackofficeViewset,
)

router = routers.DefaultRouter()
router.register("categories", CategoryViewset)
router.register("subcategories", SubCategoryViewset)
router.register(
    "backoffice/categories", CategoryBackofficeViewset, basename="backoffice-categories"
)
router.register(
    "backoffice/subcategories",
    SubCategoryBackofficeViewset,
    basename="backoffice-subcategories",
)

app_name = "category"

urlpatterns = [
    path("", include(router.urls)),
]
