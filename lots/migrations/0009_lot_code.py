# Generated by Django 3.0.5 on 2020-05-01 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0008_auto_20200501_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='code',
            field=models.BooleanField(blank=True, default=False, verbose_name='Тип игры'),
        ),
    ]