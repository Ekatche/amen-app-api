from django.db import models
from products.models import Product
from django.utils.translation import gettext_lazy as _


class Inventory(models.Model):
    """Product Inventory model"""

    product = models.OneToOneField(
        Product,
        related_name="inventory",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    quantity_sold = models.PositiveIntegerField(
        default=0, editable=True, blank=False, verbose_name=_("quantity sold")
    )
    total = models.PositiveIntegerField(
        null=False, default=0, blank=False, verbose_name=_("total quantity produced")
    )
    date_created = models.DateTimeField(
        auto_now_add=True, editable=True, verbose_name=_("Date product was created")
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date product was updated")
    )

    @property
    def get_available_quatity(self):
        return self.total - self.quantity_sold

    def __str__(self):
        return self.product

    class Meta:
        ordering = ["date_created"]
