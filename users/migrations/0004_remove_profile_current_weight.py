# Generated by Django 3.1.2 on 2020-10-15 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201015_0641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='current_weight',
        ),
    ]
