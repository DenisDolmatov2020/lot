# Generated by Django 3.0.5 on 2020-04-28 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0003_auto_20200428_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='limit_players',
            field=models.PositiveSmallIntegerField(default=3, verbose_name='Максимальное кол-во участников'),
        ),
    ]