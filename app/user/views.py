"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
    BillingAddressSerializer,
    ShippingAddressSerializer,
)
from core.models import BillingAddress, ShippingAddress


class CreateUSerView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and retrieve the authenticated user"""
        return self.request.user


class BillingAddressViewset(viewsets.ModelViewSet):
    """
    API to Manage Billing address
    """

    serializer_class = BillingAddressSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return BillingAddress.objects.filter(customer=user)


class ShippingAddressViewset(viewsets.ModelViewSet):
    """
    API to Manage Billing address
    """

    serializer_class = ShippingAddressSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return ShippingAddress.objects.filter(customer=user)
