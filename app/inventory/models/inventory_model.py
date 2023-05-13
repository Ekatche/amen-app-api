from django.db import models
from products.models import Product
from django.core.exceptions import ValidationError
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
    quantity_available = models.PositiveIntegerField(
        null=False, default=0, blank=False, verbose_name=_("total quantity in stock")
    )

    total_produced = models.PositiveIntegerField(
        null=False,
        default=0,
        blank=False,
        verbose_name=_("total purchased or produced"),
    )

    date_created = models.DateTimeField(
        auto_now_add=True, editable=True, verbose_name=_("Date product was created")
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date product was updated")
    )

    @property
    def get_available_quatity(self):
        return self.quantity_available - self.quantity_sold

    def clean(self):
        # Ensure that the total produced quantity is equal to
        # the quantity sold plus the available quantity
        if self.total_produced != self.quantity_sold + self.quantity_available:
            raise ValidationError(
                "Total produced must be equal to quantity sold + available quantity"
            )

    def save(self, *args, **kwargs):
        # Update the available quantity before saving the object
        self.quantity_available = self.total_produced - self.quantity_sold
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["date_created"]
