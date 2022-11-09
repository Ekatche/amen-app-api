from django.contrib import admin
from .models import ShoppingCart, Order, CartItem, OrderItem


class CartItemAdmin(admin.ModelAdmin):
    list_filter = [
        "date_created",
        "date_updated",
    ]
    list_display = [
        "id",
        "cart",
        "product",
        "quantity",
        "total_amount",
        "date_created",
        "date_updated",
    ]
    search_fields = ["id", "cart", "product"]


admin.site.register(CartItem, CartItemAdmin)


class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_filter = [
        "date_created",
        "date_updated",
    ]
    list_display = [
        "id",
        "customer",
        "date_created",
        "date_updated",
    ]
    search_fields = ["id", "customer"]


admin.site.register(ShoppingCart, ShoppingCartItemAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ["id", "product"]
    list_filter = ["date_created", "date_updated"]
    list_display = [
        "id",
        "product",
        "quantity",
        "order",
        "date_created",
        "date_updated",
    ]


admin.site.register(OrderItem, OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    search_fields = ["id", "customer"]
    list_filter = [
        "date_created",
        "date_updated",
        "status",
    ]
    list_display = [
        "id",
        "customer",
        "shipping",
        "amount_due",
        "date_created",
        "date_updated",
        "status",
        "reason",
    ]


admin.site.register(Order, OrderAdmin)
