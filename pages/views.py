from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

def home(request):
    loggedIn = False
    if request.user.is_authenticated:
        loggedIn = True
    return render(request, 'pages/home.html', {})





