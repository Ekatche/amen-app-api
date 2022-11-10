from django.contrib import admin
from .models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "billing",
        "order",
        "payment_method",
        "amount_due",
        "amount_paid",
        "date_created",
        "date_updated",
        "status",
    ]
    search_fields = [
        "id",
        "billing",
        "order",
    ]
    list_filter = [
        "date_created",
        "date_updated",
        "status",
        "payment_method",
    ]


admin.site.register(Invoice, InvoiceAdmin)
