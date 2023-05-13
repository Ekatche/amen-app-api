from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    search_fields = ["id", "product"]
    list_display = [
        "id",
        "product",
        "quantity_sold",
        "quantity_available",
        "total_produced",
        "date_created",
        "date_updated",
    ]
    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "product",
                "total",
            ),
        },
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True if not Inventory.objects.exists() else False

    list_filter = ["date_created", "date_updated"]


class InventoryInLine(admin.TabularInline):
    model = Inventory
    fields = (
        "id",
        "product",
        "total_produced",
    )
    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "product",
                "total_produced",
            ),
        },
    )

    raw_id_fields = ("product",)
