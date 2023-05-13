from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product, Coupons
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
    """A model that contains data for a shopping cart."""

    customer = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="shoppingcart"
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        verbose_name=_("Date ShoppingCart was created"),
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date ShoppingCart was updated")
    )

    class Meta:
        verbose_name = _("Shopping Cart")
        verbose_name_plural = _("Shopping Carts")

    def __str__(self):
        return self.id


class WishList(models.Model):
    """
    model that contains data about the customer wishes
    """

    customer = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="wishlist"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlist"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        verbose_name=_("Date the product was added as wish"),
    )

    date_updated = models.DateTimeField(
        auto_now=True,
        editable=True,
        verbose_name=_("Date the product was added as wish"),
    )


class CartItem(models.Model):
    """
    A model that contains data for an item in the shopping cart.
    """

    cart = models.ForeignKey(
        ShoppingCart,
        related_name="items",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        verbose_name=_("Date ShoppingCart was created"),
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date ShoppingCart was updated")
    )

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def __str__(self):
        return self.id


class Order(models.Model):
    """
    Order model
    """

    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="order")

    shipping = models.OneToOneField(
        ShippingAddress,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="order_address",
    )

    amount_due = models.DecimalField(
        default=0, decimal_places=2, max_digits=10, null=True, blank=True
    )

    status = models.CharField(max_length=25, default="Pending", choices=STATUS_CHOICES)

    reason = models.CharField(null=True, blank=True, max_length=150)

    date_created = models.DateTimeField(
        auto_now_add=True, editable=True, verbose_name=_("Date order was created")
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date order was updated")
    )
    coupons = models.OneToOneField(
        Coupons,
        blank=True,
        null=True,
        default="",
        related_name="orders",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):
    """A model that contains data for an item in an order."""

    order = models.ForeignKey(
        Order, related_name="order_items_order", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="order_items_product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    date_created = models.DateTimeField(
        auto_now_add=True, editable=True, verbose_name=_("Date order was created")
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date order was updated")
    )
