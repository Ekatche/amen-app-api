from django.urls import include, path
from rest_framework import routers
from .views import SubCategoryViewset, CategoryViewset

router = routers.DefaultRouter()
router.register("categories", CategoryViewset)
router.register("subcategories", SubCategoryViewset)

app_name = "category"

urlpatterns = [
    path("", include(router.urls)),
]
