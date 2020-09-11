# Generated by Django 3.0.5 on 2020-09-11 03:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('now_minutes', models.PositiveSmallIntegerField(default=0, verbose_name='Tracking online minutes')),
                ('now_ready', models.BooleanField(default=False, verbose_name='Ready online track on today')),
                ('day_minutes', models.PositiveSmallIntegerField(default=0, verbose_name='Track day minutes')),
                ('level_minutes', models.PositiveIntegerField(default=0, verbose_name='Track level minutes')),
                ('days_row', models.PositiveSmallIntegerField(default=0, verbose_name='Track days in one row time')),
                ('days_all', models.PositiveSmallIntegerField(default=0, verbose_name='Track days all')),
                ('time', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
