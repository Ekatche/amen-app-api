from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupons(models.Model):
    """
    Coupons for promotion
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Coupons Name (keep confidential). Must be unique.",
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Voucher code (keep confidential). Must be unique.",
    )
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField()
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class Promotion(models.Model):
    """
    promotion models
    """

    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=True)
    date_updated = models.DateTimeField(auto_now=True, editable=True)
    period = models.IntegerField(
        default=0, help_text=_("Number of months the promotion should last")
    )

    coupons = models.ForeignKey(
        Coupons, null=True, blank=True, on_delete=models.PROTECT
    )

    date_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")
