from django.db import models
from django.utils.translation import gettext_lazy as _
from categories.models import Category, SubCategory
from .promotion import Promotion


class Product(models.Model):
    """Product table Implemented with MPTT"""

    name = models.CharField(
        max_length=100, null=False, blank=False, verbose_name=_("product name")
    )
    slug = models.SlugField(max_length=200, db_index=True, default="")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    on_promo = models.BooleanField(default=False)
    promo = models.ForeignKey(
        Promotion, blank=True, null=True, on_delete=models.PROTECT
    )
    category = models.ManyToManyField(Category, related_name="product")
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_("subcategory"),
    )

    class Meta:
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.name
