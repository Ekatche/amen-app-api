"""
URL mappings for the user API
"""

from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    "billingaddress", views.BillingAddressViewset, basename="user-billingaddress"
)
router.register(
    "shippingaddress", views.ShippingAddressViewset, basename="user-shippingaddress"
)
router.register("user", views.Userviewset, basename="update")
router.register("create", views.CreateUserViewSet, basename="create")
router.register(
    "backoffice/user", views.BackofficeUserViewset, basename="backoffice-user"
)

app_name = "user"
urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.AuthLoginView.as_view(), name="login"),
    path("logout/", views.AuthLogoutview.as_view(), name="logout"),
    path("backoffice/login/", views.BackofficeLoginView.as_view()),
    path("backoffice/logout/", views.BackofficeLogoutView.as_view()),
    path("userChangePassword/", views.UserChangePassword.as_view()),
    # path("token/", views.CreateTokenView.as_view(), name="token"),
    # path("me/", views.ManageUserView.as_view(), name="me"),
    path("", include(router.urls)),
]
