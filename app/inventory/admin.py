from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):

    search_fields = ["id", "product"]
    list_display = [
        "id",
        "product",
        "quantity_sold",
        "total",
        "date_created",
        "date_updated",
    ]
    list_filter = ["date_created", "date_updated"]
