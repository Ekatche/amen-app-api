# Generated by Django 3.2.16 on 2022-11-09 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0003_auto_20221105_1244"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="is_active",
            field=models.BooleanField(
                default=True, verbose_name="category availability"
            ),
        ),
    ]
