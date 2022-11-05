from django.db import models
from django.utils.translation import gettext_lazy as _
from order.models import Order
from core.models import BillingAddress

CHOICES_TYPE_STATUS = (
    ("Payed", "Payed"),
    ("Refunded", "Refunded"),
    ("Failed", "Failed"),
)

CHOICES_PAYMETMETHOD = (
    ("Card", "Card"),
    ("Paypal", "Paypal"),
)


class PaymentCard(models.Model):

    card_id = models.CharField(max_length=200)
    name = models.CharField(max_length=150, null=True, blank=True, default=None)
    brand = models.CharField(max_length=30)

    exp_month = models.IntegerField()
    exp_year = models.IntegerField()

    last4 = models.CharField(max_length=4, help_text="last 4 digits of the card")

    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Invoice(models.Model):

    billing = models.OneToOneField(
        BillingAddress, on_delete=models.PROTECT, blank=True, null=True
    )

    order = models.OneToOneField(Order, on_delete=models.PROTECT, blank=True, null=True)

    payment_method = models.CharField(
        default="Card", choices=CHOICES_PAYMETMETHOD, max_length=30
    )

    amount_due = models.IntegerField(default=0)
    amount_paid = models.IntegerField(default=0)

    date_created = models.DateTimeField(
        auto_now_add=True, editable=True, verbose_name=_("Date invoice was created")
    )

    date_updated = models.DateTimeField(
        auto_now=True, editable=True, verbose_name=_("Date invoice was updated")
    )

    status = models.CharField(max_length=100, choices=CHOICES_TYPE_STATUS, default="")

    def __str__(self):
        return str(self.id)
