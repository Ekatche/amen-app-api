from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Product categories
    """

    name = models.CharField(
        max_length=100,
        unique=False,
        null=False,
        blank=False,
        verbose_name="categories name",
    )
    slug = models.SlugField(max_length=200, unique=True, db_index=True, default="")

    is_active = models.BooleanField(
        default=True, null=False, blank=False, verbose_name=_("category availability")
    )

    date_created = models.DateTimeField(
        auto_now_add=True, editable=True, verbose_name=_("Date category was created")
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date category was updated")
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")


class SubCategory(models.Model):
    """Product subcategory table"""

    name = models.CharField(
        max_length=100,
        unique=False,
        null=False,
        blank=False,
        verbose_name="subcategory name",
    )

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategory_category"
    )
    date_created = models.DateTimeField(
        auto_now_add=True, editable=True, verbose_name=_("Date category was created")
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date category was created")
    )

    def __str__(self):
        return self.name
