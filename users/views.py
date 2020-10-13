from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
def exercises(request):
    return render(request, 'users/exercises.html')

@login_required
def meals(request):
    return render(request, 'users/meals.html')