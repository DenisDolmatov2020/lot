# Generated by Django 3.0.5 on 2020-06-17 02:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_tracker_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 6, 17, 9, 49, 44, 991327)),
        ),
    ]
