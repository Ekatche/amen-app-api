from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Product(MPTTModel):
    """Product table Implemented with MPTT"""

    name = models.CharField(
        max_length=100, null=False, blank=False, verbose_name=_("product name")
    )
    price = models.DecimalField(decimal_places=2, max_digits=5)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    on_promo = models.BooleanField(default=False)

    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("parent of product"),
    )

    class MTTPMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.name
