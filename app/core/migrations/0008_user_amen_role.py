# Generated by Django 3.2.16 on 2022-11-08 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_auto_20221107_1233"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="amen_role",
            field=models.CharField(
                blank=True,
                choices=[
                    ("amen_admin", "Administrateur"),
                    ("amen_dev", "Développeur"),
                    ("amen_sales", "Commercial"),
                ],
                default=None,
                help_text="only used for backoffice purpose, not for classic user",
                max_length=20,
                null=True,
            ),
        ),
    ]
