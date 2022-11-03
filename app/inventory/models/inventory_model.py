from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product


class Inventory(models.Model):
    """Product Inventory model"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity_sold = models.IntegerField(
        default=0, editable=True, blank=False, verbose_name=_("quantity sold")
    )
    total = models.IntegerField(
        null=False, default=0, blank=False, verbose_name=_("total quantity produced")
    )
    date_created = models.DateTimeField(
        auto_now_add=True, editable=True, verbose_name=_("Date product was created")
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date product was updated")
    )

    def __str__(self):
        return self.product

    class Meta:
        ordering = ["date_created"]
