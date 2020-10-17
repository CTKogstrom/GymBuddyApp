# Generated by Django 3.1.2 on 2020-10-13 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activityLibrary', '0003_recipe_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='icon',
            field=models.ImageField(default='default.jpg', upload_to='activity_thumbnails'),
        ),
        migrations.CreateModel(
            name='ScheduledMeal',
            fields=[
                ('recipe_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activityLibrary.recipe')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('activityLibrary.recipe',),
        ),
        migrations.CreateModel(
            name='ScheduledExercise',
            fields=[
                ('exercise_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activityLibrary.exercise')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('activityLibrary.exercise',),
        ),
    ]
