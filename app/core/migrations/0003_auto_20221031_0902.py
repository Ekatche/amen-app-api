# Generated by Django 3.2.16 on 2022-10-31 09:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_is_staff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 10, 31, 9, 2, 25, 967944, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], default='m', help_text='"m" or "f"', max_length=1),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=datetime.datetime(2022, 10, 31, 9, 2, 37, 522807, tzinfo=utc), max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_prefix',
            field=models.CharField(blank=True, default='+33', max_length=10, null=True),
        ),
    ]
