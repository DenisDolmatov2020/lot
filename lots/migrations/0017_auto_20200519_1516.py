# Generated by Django 3.0.5 on 2020-05-19 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0016_auto_20200519_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='Подписка', max_length=32)),
            ],
        ),
        migrations.RemoveField(
            model_name='condition',
            name='lot',
        ),
        migrations.AddField(
            model_name='lot',
            name='condition',
            field=models.ManyToManyField(related_name='conditions_set', to='lots.Condition'),
        ),
        migrations.DeleteModel(
            name='Actions',
        ),
        migrations.AddField(
            model_name='condition',
            name='actions',
            field=models.ManyToManyField(related_name='actions_set', to='lots.Action'),
        ),
    ]
