# Generated by Django 3.0.5 on 2020-06-20 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0021_auto_20200610_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotnumber',
            name='won',
            field=models.BooleanField(default=False, verbose_name='winner'),
        ),
    ]
