from django.db import models
from django.utils.translation import gettext_lazy as _
from categories.models import Category


class Product(models.Model):
    """Product table Implemented with MPTT"""

    name = models.CharField(
        max_length=100, null=False, blank=False, verbose_name=_("product name")
    )
    price = models.DecimalField(decimal_places=2, max_digits=5)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    on_promo = models.BooleanField(default=False)

    category = models.ManyToManyField(Category, related_name="product_category")

    def __str__(self):
        return self.name
