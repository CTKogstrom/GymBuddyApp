from django import forms
from django.contrib.auth.models import User
from .models import ScheduledExercise, ScheduledMeal


class ScheduleMealForm(forms.ModelForm):
    class Meta:
        model = ScheduledMeal
        fields = ['recipe', 'date']


class ScheduleExerciselForm(forms.ModelForm):
    class Meta:
        model = ScheduledExercise
        fields = ['exercise', 'date']
