from django.contrib import admin
from .models import Category, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ["id", "name", "slug", "is_active", "date_created", "date_updated"]
    list_display = ["id", "name", "slug", "is_active", "date_created", "date_updated"]
    list_filter = ["date_created", "date_updated", "is_active"]
    search_fields = ["name", "slug"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    fields = ["id", "name", "category", "date_created", "date_updated"]
    list_display = ["id", "name", "category", "date_created", "date_updated"]
    list_filter = ["date_created", "date_updated"]
    search_fields = ["name", "category"]
