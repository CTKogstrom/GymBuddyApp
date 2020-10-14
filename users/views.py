from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
import json, os
from .forms import UserRegisterForm
from .forms import ProfileForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form' : form})

def login2(request, user):
    return render(request, 'users/login.html')

@login_required
def profile(request):
    if request.method == 'POST' and 'submit_form' in request.POST:
        profForm = ProfileForm(request.POST)
        if profForm.is_valid:
            stillValid = True
            if profForm.cleaned_data['daily_cal_in'] < 0:
                messages.error(request, "Please enter a valid number of calories.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['daily_carbs'] < 0:
                messages.error(request, "Please enter a valid number of carbohydrates.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['daily_fat'] < 0:
                messages.error(request, "Please enter a valid number of fats.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['daily_protein'] < 0:
                messages.error(request, "Please enter a valid number of proteins.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['goal_weight_change'] < 0:
                messages.error(request, "Please enter a valid weight.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['activity_level'] < 0:
                messages.error(request, "Please enter a valid activity level.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['current_weight'] < 0:
                messages.error(request, "Please enter a valid weight.", extra_tags='danger')
                stillValid = False
            if stillValid:
                prof = Profile(daily_cal_in=profForm.cleaned_data['daily_cal_in'],daily_carbs=profForm.cleaned_data['daily_carbs'],daily_fat=profForm.cleaned_data['daily_fat'],
                    daily_protein=profForm.cleaned_data['daily_protein'],goal_weight_change=profForm.cleaned_data['goal_weight_change'],activity_level=profForm.cleaned_data['activity_level'],
                    current_weight=profForm.cleaned_data['current_weight'])
                prof.save()
                messages.succes(request, "Successfully updated profile!", extra_tags='success')
        else:
            messages.error(request, "Please reenter valid information.", extra_tags='danger')
    form = ProfileForm()
    context = {
        'loggedIn': False,
        'form': form
    }
    if request.user.is_authenticated:
        context['loggedIn'] = True
    return render(request, 'users/profile.html', context)

@login_required
def weight(request):
    return render(request, 'users/weight.html')
  
@login_required
def macros(request):
    return render(request, 'users/macros.html')
    
@login_required
def exercises(request, active_exercises=0):
    exercise_list = []

    with open(os.path.dirname(os.path.realpath(__file__)) + '/Exercises.json') as f:
        data = json.load(f)

    if (active_exercises == 100):
        exercise_list = data

    context = {
            'exercises': exercise_list,
            'title': 'Exercises',
            'active_exercise': active_exercises, #exercise_list[0].group,
    }
    return render(request, 'users/exercises.html', context)

@login_required
def meals(request):
    return render(request, 'users/meals.html')

