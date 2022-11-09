from django.db import models
from django.utils.translation import gettext_lazy as _
from . import Product


class Media(models.Model):
    """
    Media for the products
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("product image"),
        upload_to="images/",
        default="images/default.png",
        help_text=_("format: required, default-default.png"),
    )
    date_created = models.DateTimeField(
        auto_now_add=True, editable=True, verbose_name=_("Date image was uploaded")
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date image was updated")
    )

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")
