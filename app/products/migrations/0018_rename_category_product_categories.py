# Generated by Django 4.1.2 on 2022-11-16 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0017_alter_coupons_code"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="category",
            new_name="categories",
        ),
    ]
