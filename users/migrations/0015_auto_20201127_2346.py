# Generated by Django 3.1.2 on 2020-11-27 23:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0014_delete_liftrecord'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LiftRecord2',
            new_name='LiftRecord',
        ),
    ]
