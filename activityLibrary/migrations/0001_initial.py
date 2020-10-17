# Generated by Django 3.1.2 on 2020-10-12 22:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('icon', models.ImageField(upload_to='')),
                ('scheduled_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activityLibrary.activity')),
                ('demo', models.URLField()),
                ('targetMuscle', models.CharField(max_length=100)),
            ],
            bases=('activityLibrary.activity',),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activityLibrary.activity')),
                ('calories', models.IntegerField()),
                ('carbs', models.IntegerField()),
                ('fat', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('cook_duration_mins', models.IntegerField()),
            ],
            bases=('activityLibrary.activity',),
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('vegetarian', models.BooleanField()),
                ('veagan', models.BooleanField()),
                ('recipes', models.ManyToManyField(blank=True, to='activityLibrary.Recipe')),
            ],
        ),
    ]
