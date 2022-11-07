from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product
from core.models import User, ShippingAddress


STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Awaiting Fulfillment", "Awaiting Fulfillment"),
    ("Shipped", "Shipped"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
)


class ShoppingCart(models.Model):

    products = models.ForeignKey(
        Product,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="shoppingcart",
    )

    customer = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="shoppingcart"
    )

    quantity = models.IntegerField()

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        verbose_name=_("Date ShoppingCart was created"),
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date ShoppingCart was updated")
    )

    amount_due = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Shopping Cart")
        verbose_name_plural = _("Shopping Carts")


class Order(models.Model):
    """
    Order model
    """

    products = models.ForeignKey(
        Product, blank=True, null=True, on_delete=models.PROTECT
    )

    shipping = models.OneToOneField(
        ShippingAddress,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="order_address",
    )

    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="order")

    quantity = models.IntegerField()

    shoppingcart = models.OneToOneField(
        ShoppingCart,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="order",
        verbose_name="Shopping Card",
    )

    amount_due = models.IntegerField(default=0)

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
