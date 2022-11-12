# Generated by Django 3.2.16 on 2022-11-11 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_user_amen_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billingaddress",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="billingaddress",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shippingaddress",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
