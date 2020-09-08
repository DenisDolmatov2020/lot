# Generated by Django 3.0.5 on 2020-05-01 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0005_auto_20200429_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='is_free',
            field=models.BooleanField(blank=True, default=True, verbose_name='Свободные места'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, verbose_name='Active game'),
        ),
    ]
