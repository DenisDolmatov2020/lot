# Generated by Django 3.0.5 on 2020-05-18 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0012_auto_20200515_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='condition',
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='Youtube', max_length=32)),
                ('link', models.URLField()),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Лот', to='lots.Lot')),
            ],
        ),
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='Условие', max_length=32)),
                ('link', models.URLField()),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Название', to='lots.Lot')),
            ],
        ),
    ]
