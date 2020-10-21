from django.db import models
from django.contrib.auth.models import User
from activityLibrary.models import Exercise
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    daily_cal_in = models.IntegerField(default=0)
    daily_carbs = models.IntegerField(default=0)
    daily_fat = models.IntegerField(default=0)
    daily_protein = models.IntegerField(default=0)
    starting_weight = models.IntegerField(default=0)
    goal_weight_change = models.IntegerField(default=0)
    activity_level = models.DecimalField(max_digits=2, decimal_places=1,default=1.5)

    def __str__(self):
        return f'{self.user.username} Profile'


class WeightRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lbs = models.IntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.lbs} on {self.date}"


class LiftRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(blank=True, null=True)
    reps_per_set = models.IntegerField(blank=True, null=True)
    date = models.DateField()


class LiftRecord2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    weight = models.IntegerField(blank=True, null=True)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    date = models.DateField(default=timezone.now)


class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    carbs = models.IntegerField()
    fats = models.IntegerField()
    protein = models.IntegerField()
    calories = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
