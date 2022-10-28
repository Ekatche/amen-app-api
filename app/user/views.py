"""
Views for the user APO
"""

from rest_framework import generics
from .serializers import UserSerializer


class CreateUSerView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer
