# Generated by Django 3.0.5 on 2020-06-20 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_user', '0016_auto_20200610_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='diamonds',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name=''),
        ),
    ]
