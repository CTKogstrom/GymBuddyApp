# Generated by Django 3.1.2 on 2020-10-13 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activityLibrary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('vegetarian', models.BooleanField()),
                ('vegan', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='activity',
            name='scheduled_date',
        ),
        migrations.DeleteModel(
            name='Ingredients',
        ),
    ]
