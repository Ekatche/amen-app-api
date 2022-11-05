# Generated by Django 3.2.16 on 2022-11-04 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0007_product_subcategory"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="coupons",
            options={"verbose_name": "Coupon", "verbose_name_plural": "Coupons"},
        ),
        migrations.AddField(
            model_name="promotion",
            name="date_start",
            field=models.DateField(blank=True, null=True),
        ),
    ]