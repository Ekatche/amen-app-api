# Generated by Django 3.2.16 on 2022-11-10 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0015_alter_product_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="inventory",
        ),
    ]
