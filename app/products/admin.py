from django.contrib import admin
from .models.product import Product
from .models.media import Media
from .models.promotion import Promotion, Coupons


# Register your models_legacy here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "subcategory", "price", "is_available", "on_promo"]
    list_filter = ["is_available", "on_promo"]
    search_fields = ["name", "category", "subcategory"]


admin.site.register(Product, ProductAdmin)


class MediaAdmin(admin.ModelAdmin):
    list_display = ["product", "date_created", "date_updated"]
    list_filter = ["date_created", "date_updated"]
    search_fields = ["product"]


admin.site.register(Media, MediaAdmin)


class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "date_created",
        "date_updated",
        "period",
        "coupons",
        "date_end",
    ]
    list_filter = ["date_created", "date_updated"]
    search_fields = ["name"]


admin.site.register(Promotion, PromotionAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "date_created",
        "date_updated",
        "discount",
        "name",
        "is_active",
    ]
    list_filter = ["is_active", "date_created", "date_updated"]
    search_fields = ["code"]


admin.site.register(Coupons, CouponAdmin)
