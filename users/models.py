from django.db import models
from django.contrib.auth.models import User
from activityLibrary.models import Exercise

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    daily_cal_in = models.IntegerField()
    daily_carbs = models.IntegerField()
    daily_fat = models.IntegerField()
    daily_protein = models.IntegerField()
    goal_weight_change = models.IntegerField()
    activity_level = models.DecimalField(max_digits=2, decimal_places=1)
    current_weight = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} Profile'

class WeightRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lbs = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username}: {self.lbs} on {self.date}"

class LiftRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(blank=True, null=True)
    reps_per_set = models.IntegerField(blank=True, null=True)
    date = models.DateField()


