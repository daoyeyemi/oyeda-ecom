from oyeda.forms import CreateUser
from django.shortcuts import render, redirect
from .models import Shoe
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUser

def home(request):
    context = {
        'shoes' : Shoe.objects.all()
    }
    return render(request, 'home.html', context)

def products(request):
    context = {
        'shoes' : Shoe.objects.all()
    }
    return render(request, 'products.html', context)

def login(request):
    context = {
        # 'form' : form
    }
    return render(request, 'login.html', context)

def signup(request):
    form = CreateUser()

    if request.method == 'POST':
        form = CreateUser(request.POST)
        # forms are primarily used to validate data so the is.valid() function returns 
        # boolean stating whether or not value is true
        if form.is_valid(): 
            # .save() creates and saves object to database; if object already exists, it
            # updates it instead
            form.save()

    context = {
        'form' : form
    }
    return render(request, 'signup.html', context)

class ShoeDetailView(DetailView):
    model = Shoe
    template_name = 'individual-product.html'

