from django.urls import include, path
from rest_framework import routers
from .views import SubCategoryViewset, CategoryViewset

router = routers.DefaultRouter()
router.register("category", CategoryViewset)
router.register("subcategory", SubCategoryViewset)

urlpatterns = [
    path("", include(router.urls)),
]
