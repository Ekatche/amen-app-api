from django.urls import include, path
from rest_framework import routers
from .views import InventoryViewSet

router = routers.DefaultRouter()
router.register("inventory", InventoryViewSet)
app_name = "inventory"
urlpatterns = [path("", include(router.urls))]
