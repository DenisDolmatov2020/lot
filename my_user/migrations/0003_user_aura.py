# Generated by Django 3.0.5 on 2020-05-10 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_user', '0002_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='aura',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='Аура подписчика'),
        ),
    ]