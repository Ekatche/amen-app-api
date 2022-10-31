"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

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
            first_name=extra_field.get("first_name", None),
            last_name=extra_field.get("last_name", None),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **estra_field):
        """Create and return a new super user"""
        user = self.create_user(email, password)
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

    USERNAME_FIELD = "email"
