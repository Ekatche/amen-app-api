from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
urlpatterns = [
    path("backoffice/get-data/counts/", views.DataPerMonthView.as_view()),
    path("backoffice/get-data/stats/", views.GetdescriptiveData.as_view()),
    path("backoffice/get-data/products/", views.GetDataPerProduct.as_view()),
]
