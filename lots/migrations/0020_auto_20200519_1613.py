# Generated by Django 3.0.5 on 2020-05-19 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0019_remove_condition_actions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='conditions',
        ),
        migrations.AddField(
            model_name='condition',
            name='lot',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, related_name='condition_set', to='lots.Lot'),
            preserve_default=False,
        ),
    ]
