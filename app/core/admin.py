"""
Django admin customisations
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class UserAdmin(BaseUserAdmin):
    """define the admin page for user"""

    ordering = ["id"]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "date_created",
        "date_updated",
    ]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal informations"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth_date",
                    "gender",
                    "phone_prefix",
                    "phone_number",
                )
            },
        ),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "amen_role")},
        ),
        (_("Imporant dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]

    add_fieldsets = (
        (
            None,
            {
                # wide make the page better
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ["email", "first_name", "last_name", "id"]


admin.site.register(models.User, UserAdmin)


class JwtTokenAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "user",
        "token_access",
        "token_refresh",
        "ip_address",
        "user_agent",
        "is_logged_out",
        "date_modified",
        "date_created",
    ]


admin.site.register(models.JwtToken, JwtTokenAdmin)


class ShippingAddressAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "customer", "building_number", "street", "city", "postcode"]
    add_fieldsets = (
        (
            None,
            {
                # wide make the page better
                "classes": ("wide",),
                "fields": (
                    "customer",
                    "building_number",
                    "street",
                    "city",
                    "postcode",
                ),
            },
        ),
    )


admin.site.register(models.ShippingAddress, ShippingAddressAdmin)


class BillingAddressAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "customer", "building_number", "street", "city", "postcode"]
    add_fieldsets = (
        (
            None,
            {
                # wide make the page better
                "classes": ("wide",),
                "fields": (
                    "customer",
                    "building_number",
                    "street",
                    "city",
                    "postcode",
                ),
            },
        ),
    )


admin.site.register(models.BillingAddress, BillingAddressAdmin)
