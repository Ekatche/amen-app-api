from django.contrib import admin
from .models import ShoppingCart, Order, CartItem, OrderItem

admin.site.register(CartItem)
admin.site.register(ShoppingCart)
admin.site.register(OrderItem)
admin.site.register(Order)
