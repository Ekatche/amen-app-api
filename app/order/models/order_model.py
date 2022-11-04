from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product
from core.models import User, Shipping


STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Awaiting Fulfillment", "Awaiting Fulfillment"),
    ("Shipped", "Shipped"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
)


class ShoppingCard(models.Model):

    products = models.ForeignKey(
        Product, blank=True, null=True, on_delete=models.PROTECT
    )

    customer = models.OneToOneField(User, on_delete=models.PROTECT)

    quantity = models.IntegerField()

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        verbose_name=_("Date ShoppingCard was created"),
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date ShoppingCard was updated")
    )

    is_validated = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Shopping Card")
        verbose_name_plural = _("Shopping Cards")


class Order(models.Model):
    """
    Order model
    """

    products = models.ForeignKey(
        Product, blank=True, null=True, on_delete=models.PROTECT
    )

    shipping = models.OneToOneField(
        Shipping, blank=True, null=True, on_delete=models.PROTECT
    )

    customer = models.ForeignKey(User, on_delete=models.PROTECT)

    quantity = models.IntegerField()

    shoppingcard = models.OneToOneField(
        ShoppingCard,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Shopping Card",
    )

    status = models.CharField(max_length=25, default="Pending", choices=STATUS_CHOICES)

    reason = models.CharField(null=True, blank=True, max_length=150)

    date_created = models.DateTimeField(
        auto_now_add=True, editable=True, verbose_name=_("Date order was created")
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date order was updated")
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
