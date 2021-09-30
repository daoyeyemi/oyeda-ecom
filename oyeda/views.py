from oyeda.forms import CreateUser
from django.shortcuts import render, redirect
from .models import Shoe
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model 

# request is an object django uses to send metadata throughout the project

def home(request):
    
    current_user = request.user

    print(current_user)

    username = current_user.first_name
    
    print(username)

    # User = get_user_model()

    # users = User.objects.all()
        
    # select_name = users.get(username=username)

    # print(select.first_name)
    # print(users)


    context = {
        'shoes' : Shoe.objects.all(),
        'username' : username
    }

    return render(request, 'home.html', context)

def checkout(request):
    return render(request, 'checkout.html')

def order_summary(request):
    return render(request, 'order-summary.html')

def products(request):
    context = {
        'shoes' : Shoe.objects.all()
    }
    return render(request, 'products.html', context)

# @login_required basically requires user to be logged in to access page; decorator would disallow
# me from using the following function or being on the home page if I wasn't logged in

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
            messages.success(request, 'user profile for ' + user + ' was successfully created')
            return redirect('oyeda:login')
    
    context = {
        'form' : form
    }
    
    return render(request, 'signup.html', context)

def user_logout(request):
    # when logout is called session data is deleted and 
    logout(request)
    print(request.user)
    return redirect('oyeda:login')

def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # authenticate() check credentials it gets and returns 
        # object that matches the credentials if credentials are valid
        # if they're not valid, it should return None
        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            # login takes in request and user object
            # saves the user ID in the session, using django's
            # session framework
            login(request, user)
            return redirect('oyeda:home')

        else:
            # error added to object and displayed if called upon 
            # in template 
            messages.error(request, 'Wrong username or password entered.')

    context = {

    }

    return render(request, 'login.html', context)


class ShoeDetailView(DetailView):
    model = Shoe
    template_name = 'individual-product.html'