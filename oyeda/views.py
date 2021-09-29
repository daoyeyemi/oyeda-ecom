from oyeda.forms import CreateUser
from django.shortcuts import render, redirect
from .models import Shoe
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 

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
            # take saved information from form and withdraw 
            user = form.cleaned_data.get('username')
            
            print(user)
            
            messages.success(request, 'User profile for ' + user + ' was successfully created')
            
            return redirect('oyeda:login')
    
    context = {
        'form' : form
    }
    
    return render(request, 'signup.html', context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # authenticate() check credentials it gets and returns 
        # object that matches the credentials if credentials are valid
        # if they're not valid, it should return None
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login takes in request and user object
            # saves the user ID in the session, using django's
            # session framework
            login(request, user)
            redirect('oyeda:login')

    context = {

    }

    return render(request, 'login.html', context)


class ShoeDetailView(DetailView):
    model = Shoe
    template_name = 'individual-product.html'

