from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.Form):
    daily_cal_in = forms.IntegerField(label="Daily Calories")
    daily_carbs = forms.IntegerField(label="Daily Carbohydrates")
    daily_fat = forms.IntegerField(label="Daily Fat")
    daily_protein = forms.IntegerField(label="Daily Protein")
    goal_weight_change = forms.IntegerField(label="Goal Weight")
    activity_level = forms.DecimalField(label="Activity Level", max_digits=2, decimal_places=1)
    current_weight = forms.IntegerField(label="Current Weight")
