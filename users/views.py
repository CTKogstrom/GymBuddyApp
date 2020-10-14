from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json, os
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            #message does not appear
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form' : form})

def login(request):
    return render(request, 'users/login.html')

@login_required
def profile(request):
    return render(request, 'users/profile.html')

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

