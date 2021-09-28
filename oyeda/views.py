from django.shortcuts import render, redirect
from .models import Shoe
from django.views.generic import DetailView

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
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

class ShoeDetailView(DetailView):
    model = Shoe
    template_name = 'individual-product.html'

