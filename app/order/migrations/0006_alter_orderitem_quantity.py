# Generated by Django 3.2.16 on 2022-11-08 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0005_auto_20221108_1416"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]