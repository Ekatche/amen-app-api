"""
URL mappings for the user API
"""

from django.urls import path
from . import views

app_name = "user"
urlpatterns = [path("create/", views.CreateUSerView.as_view(), name="create")]
