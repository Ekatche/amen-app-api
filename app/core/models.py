"""
Database models for user
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _

CHOICES_GENDER = (("m", "Male"), ("f", "Female"))


class UserManager(BaseUserManager):
    """Manger for user"""

    def create_user(self, email, password=None, **extra_field):
        """create and save a new user"""
        if not email:
            # ensure that the email address is written
            raise ValueError("User must have an email address.")

        user = self.model(
            email=self.normalize_email(email),
            first_name=extra_field.get("first_name", "Test"),
            last_name=extra_field.get("last_name", "Name"),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **estra_field):
        """Create and return a new superuser"""
        user = self.create_user(
            email,
            password,
            first_name=estra_field.get("first_name", "Test"),
            last_name=estra_field.get("last_name", "Name"),
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # additional information since it will be an e-commerce api
    birth_date = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=CHOICES_GENDER, default="m", help_text='"m" or "f"'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    phone_prefix = models.CharField(max_length=10, default="+33", null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="shippingaddress",
        null=True,
        blank=True,
    )
    building_number = models.CharField(
        max_length=100, blank=True, default="", null=True
    )
    street = models.CharField(max_length=100, blank=True, null=True, default="")
    city = models.CharField(max_length=100, blank=True, null=True, default="")
    postcode = models.CharField(max_length=10, blank=True, null=True, default="")

    class Meta:
        verbose_name = _("shipping address")
        verbose_name_plural = _("shipping addresses")

    @property
    def address(self) -> str:
        if self.building_number:
            if self.street and self.postcode and self.city:
                return (
                    self.building_number
                    + " "
                    + self.street
                    + " "
                    + self.postcode
                    + " "
                    + self.city
                )
            elif self.street and self.postcode and not self.city:
                return self.building_number + " " + self.street + " " + self.postcode
            elif self.street and not self.postcode and self.city:
                return self.building_number + " " + self.street + " " + self.city
            else:
                return ""
        else:
            if self.street and self.postcode and self.city:
                return self.street + " " + self.postcode + " " + self.city
            elif self.street and self.postcode and not self.city:
                return self.street + " " + self.postcode
            elif self.street and not self.postcode and self.city:
                return self.street + " " + self.city
            else:
                return ""


class BillingAddress(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="billingaddress",
        null=True,
        blank=True,
    )
    building_number = models.CharField(
        max_length=100, blank=True, default="", null=True
    )
    street = models.CharField(max_length=100, blank=True, null=True, default="")
    city = models.CharField(max_length=100, blank=True, null=True, default="")
    postcode = models.CharField(max_length=10, blank=True, null=True, default="")

    class Meta:
        verbose_name = _("billing address")
        verbose_name_plural = _("billing addresses")

    @property
    def address(self) -> str:
        if self.building_number:
            if self.street and self.postcode and self.city:
                return (
                    self.building_number
                    + " "
                    + self.street
                    + " "
                    + self.postcode
                    + " "
                    + self.city
                )
            elif self.street and self.postcode and not self.city:
                return self.building_number + " " + self.street + " " + self.postcode
            elif self.street and not self.postcode and self.city:
                return self.building_number + " " + self.street + " " + self.city
            else:
                return ""
        else:
            if self.street and self.postcode and self.city:
                return self.street + " " + self.postcode + " " + self.city
            elif self.street and self.postcode and not self.city:
                return self.street + " " + self.postcode
            elif self.street and not self.postcode and self.city:
                return self.street + " " + self.city
            else:
                return ""
