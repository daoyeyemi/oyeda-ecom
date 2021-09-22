from django.shortcuts import render, redirect
from .models import Shoe

def home(request):
    context = {
        'shoes' : Shoe.objects.all()
    }

    return render(request, 'home.html', context)