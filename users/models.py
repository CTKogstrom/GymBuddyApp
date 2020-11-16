from django.db import models
from django.contrib.auth.models import User
from activityLibrary.models import Exercise
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_activity_level(value):
    if value < 1.2 or value > 2.1:
        raise ValidationError(
            gettext_lazy('%(value)d is not in the range 1.2-2.1'),
            params={'value':value}
        )

def validate_goal_weight_change(value):
    if value < -1 or value > 1:
        raise ValidationError(
            gettext_lazy("$(value)s is not in the range (-1) - (1) "),
            params={'value': value}
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    daily_cal_in = models.IntegerField(default=2000)
    daily_carbs = models.IntegerField(default=0)
    daily_fat = models.IntegerField(default=0)
    daily_protein = models.IntegerField(default=0)
    weight = models.IntegerField(default=150)
    pct_diet_carbs = models.IntegerField(default=45)
    pct_diet_fat = models.IntegerField(default=20)
    pct_diet_prot = models.IntegerField(default=35)
    goal_weight_change = models.DecimalField(max_digits=3, decimal_places=2, default=-1, validators=[validate_goal_weight_change])
    activity_level = models.DecimalField(max_digits=2, decimal_places=1,default=1.5,
                                         help_text="Must be a value betwen 1.2 and 2.1",
                                         validators=[validate_activity_level])
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
