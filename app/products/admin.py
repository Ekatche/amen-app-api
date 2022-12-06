from django.contrib import admin
from inventory.admin import InventoryInLine

from .models.media import Media
from .models.product import Product
from .models.promotion import Promotion, Coupons
from .tasks import promotion_price, promotion_management


# Register your models_legacy here.


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = [
        "name",
        "slug",
        "subcategory",
        "price",
        "is_available",
        "on_promo",
        "promo",
        "promo_price",
    ]
    list_filter = ["is_available", "on_promo"]
    search_fields = ["name", "category", "subcategory"]
    list_editable = ["price", "is_available", "on_promo", "promo"]
    inlines = (InventoryInLine,)
    prepopulated_fields = {"slug": ("name",)}
    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "name",
                "slug",
                "price",
                "category",
                "subcategory",
                "description",
                "is_available",
                "on_promo",
            ),
        },
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        promotion_price.delay(obj.promo.coupons.discount, obj.promo.id)


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
        "is_active",
        "is_schedule",
        "date_start",
        "date_end",
    ]
    list_filter = ["date_created", "date_updated"]
    search_fields = ["name"]

    def save_model(self, request, obj, form, change):
        # override save for promotion and added celery tasks
        super().save_model(request, obj, form, change)
        promotion_management.delay()


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
