# Generated by Django 3.0.5 on 2020-09-11 03:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='condition',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='condition_set', to='lots.Lot'),
        ),
    ]
