from django.shortcuts import render
from .models import Activity

def search(request):
    context = {
        'results': Activity.objects.all()
    }