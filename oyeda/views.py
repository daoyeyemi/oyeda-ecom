from oyeda.forms import CreateUser
from django.shortcuts import render, redirect, get_object_or_404
from .models import Shoe, OrderList, OrderedItem
from django.views.generic import DetailView, View
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUser
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, get_user_model 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# request is an object django uses to send metadata throughout the project
# request.user.first_name

def home(request):    
    current_user = request.user
    print(current_user)
    # username = current_user.first_name    
    # print(username)
    # User = get_user_model()
    # users = User.objects.all()        
    # select_name = users.get(username=username)
    # print(select.first_name)
    # print(users)
    yooooo = get_user_model()
    yuhhh = yooooo.objects.all()
    # hmmmmm = yuhhh.get(username=current_user.username)
    # print(hmmmmm)

    context = {
        'shoes' : Shoe.objects.all(),
        # 'username' : username,
        # 'logout' : user_logout
    }

    return render(request, 'home.html', context)

def user_logout(request):
    # when logout is called session data is deleted and 
    logout(request)
    print(request.user)
    print('Hell yeahhhhhhh')
    # return redirect('oyeda:login')
    return render(request, 'home.html')



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

# LoginRequiredMixin is the class equivalent of @login_required for functions
# class inherits      
class OrderSummary(View, LoginRequiredMixin):
    # custom get function usually used when using a class-based view 
    # (assuming just a matter of good django ettiquete?)
    # -------
    # self represents the instance of the class
    # using self basically gives access to all the methods and attributes 
    # important to know that this is the default when you're calling a method 
    # within a class 
    def get(self, request):
        # try-except clause calls statement between try and except clause
        # if exception occurs and it matches the exception, then the except 
        # clause is executed
        # cannot use get() when multiple objects match the criteria, must instead use filter
        try:
            order = OrderList.objects.filter(user=request.user, ordered=False)
            context = {
                'order' : order
            }
            return render(request, 'order-summary.html', context)

        except ObjectDoesNotExist:
        # ObjectDoesNotExist for all exceptions to get(); used often w try 
        # and except
            # messages.warning(request, 'No orders in the works at the moment.')
            print("Nope...")
            return redirect('/')

# def remove_from_cart(request):
    # shoe_to_remove = 

# get_object_or_404()
# get_or_create()
# all we're really doing is changing the quantity of an item in the order
def add_to_cart(request, slug):
    try:
        item = Shoe.objects.get(slug=slug)
        order_list = OrderList.objects.get(user=request.user, ordered=False)
        order_item = OrderedItem.objects.get(item=item)
        print(order_list.items)
        print(order_item)
    # for many-to-many relationships add() accepts model instances or field values
        print(order_item.quantity)
        order_item.quantity += 1
        print(order_item.quantity)
        order_item.save()
        return redirect("oyeda:order-summary")
    except OrderedItem.DoesNotExist:
        print("Item hasn't been ordered yet.")
        new_order_item = OrderedItem.objects.create(item=item)
        print(new_order_item)
        order_list.item.add(new_order_item)
        return redirect("oyeda:order-summary")
    except OrderList.DoesNotExist:
        print("No order list for you sir / ma'am")
        new_order = OrderList.objects.create(user=request.user)
        print(new_order)
        new_order.items.add(order_item)
        print(new_order)

        return redirect("oyeda:order-summary")
        # return render(request, 'order-summary.html')    
    # try:
    #     order = OrderList.objects.get(user=request.user, ordered=False)
        
   
    #     return redirect('oyeda:order-summary')

    # except OrderList.DoesNotExist:
    #     new_order = OrderList.objects.create(user=request.user, quantity=1, ordered=False)
    #     new_order.save()
    #     return redirect('oyeda:order-summary') 
    # # retrieve object that has slug that is equal to the slug
    # # getting data in the Shoe model and getting the slug that fits
    # # shoe = get_object_or_404(Shoe, slug=slug)
    # # shoe_to_add = Shoe.objects.filter(slug=slug)
    # # .add() should only be used when dealing with many-to-many relationships
    # except OrderList.MultipleObjectsReturned:
    #     order = OrderList.objects.filter(user=request.user, ordered=False)

    #     return redirect('oyeda:order-summary')
