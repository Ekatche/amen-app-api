"""
URL mappings for the user API
"""

from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("billingaddress", views.BillingAddressViewset, basename="user")
router.register("shippingaddress", views.ShippingAddressViewset, basename="user")
router.register("user", views.Userviewset, basename="user")
router.register("user", views.CreateUserViewSet)

app_name = "user"
urlpatterns = [
    path("signup/", views.SignUpView.as_view()),
    path("login/", views.AuthLoginView.as_view()),
    path("logout/", views.AuthLogoutview.as_view()),
    path("userChangePassword/", views.UserChangePassword.as_view()),
    # path("token/", views.CreateTokenView.as_view(), name="token"),
    # path("me/", views.ManageUserView.as_view(), name="me"),
    path("", include(router.urls)),
]
