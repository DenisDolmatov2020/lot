# Generated by Django 3.0.5 on 2020-05-19 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0017_auto_20200519_1516'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lot',
            old_name='condition',
            new_name='conditions',
        ),
    ]