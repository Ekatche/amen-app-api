from django.urls import include, path
from rest_framework import routers
from .views import InventoryBackofficeViewSet

router = routers.DefaultRouter()
router.register("inventory", InventoryBackofficeViewSet)
app_name = "inventory"
urlpatterns = [path("", include(router.urls))]
