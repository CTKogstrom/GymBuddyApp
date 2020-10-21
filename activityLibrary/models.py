from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils import timezone

WORKOUT_CATEGORIES = [
    ('All', 'All'),
    ('Cardio', 'Cardio'),
    ('Chest', 'Chest'),
    ('Abdominals', 'Abdominals'),
    ('Obliques', 'Obliques'),
    ('Lats', 'Lats'),
    ('Trapezius', 'Trapezius'),
    ('Shoulders', 'Shoulders'),
    ('Triceps', 'Triceps'),
    ('Biceps', 'Biceps'),
    ('Forearms', 'Forearms'),
    ('Hips', 'Hips'),
    ('Buttocks', 'Buttocks'),
    ('Quads', 'Quads'),
    ('Hamstrings', 'Hamstrigns'),
    ('Calves', 'Calves'),
]

MEAL_CATEGORIES = [
    ('All', 'All'),
    ('Breakfast','Breakfast'),
    ('Lunch','Lunch'),
    ('Dinner', 'Dinner'),
    ('Snacks', 'Snacks'),
    ('Dessert', 'Dessert'),
]


def get_default_exercise():
    return Exercise.objects.get_or_create(title='GenericExercise')


def get_default_meal():
    return Recipe.objects.get_or_create(title='GenericRecipe',)


class Activity(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    icon = models.ImageField(default='default.jpg',upload_to='activity_thumbnails')


class Exercise(Activity):
    demo = models.URLField()
    category = models.CharField(max_length=100,choices=WORKOUT_CATEGORIES,default='All')

    def __str__(self):
        return self.title


class ScheduledExercise(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    vegetarian = models.BooleanField()
    vegan = models.BooleanField()


class Recipe(Activity):
    calories = models.IntegerField()
    category = models.CharField(max_length=30,choices=MEAL_CATEGORIES,default='All')
    carbs = models.IntegerField()
    fat = models.IntegerField()
    protein = models.IntegerField()
    cook_duration_mins = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient, blank=True)

    def __str__(self):
        return self.title


class ScheduledMeal(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,null=True)



