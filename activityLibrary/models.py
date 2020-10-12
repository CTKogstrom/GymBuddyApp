from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Activity(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    icon = models.ImageField()
    scheduled_date = models.DateField(default=timezone.now)
    scheduled_by = models.ForeignKey(User, on_delete=models.SET_NULL)


class Exercise(Activity):
    demo = models.URLField()
    targetMuscle = models.CharField(max_length=100)


class Recipe(Activity):
    calories = models.IntegerField()
    carbs = models.IntegerField()
    fat = models.IntegerField()
    protein = models.IntegerField()
    cook_duration_mins = models.IntegerField()


class Ingredients(models.Model):
    name = models.CharField(max_length=100)
    vegetarian = models.BooleanField()
    veagan = models.BooleanField()
    recipes = models.ManyToManyField(Recipe, blank = True)


