from oyeda.forms import CreateUser
from django.shortcuts import render, redirect, get_object_or_404

from oyedaecom.settings import STRIPE_PRIVATE_KEY
from .models import Payment, Shoe, OrderList, OrderedItem
from django.views.generic import DetailView, View
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUser, CheckoutForm, PaymentForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, get_user_model 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . models import BillingAddress, ShippingAddress, OrderList, Brand
import stripe
from django.conf import settings

# request is an object django uses to send metadata throughout the project
# request.user.first_name
stripe.api_key = settings.STRIPE_PRIVATE_KEY

class CheckoutView(View):
    # gets data 
    def get(self, request):
        try:
            order = OrderList.objects.get(user=request.user, ordered=False)

            form = CheckoutForm()

            context = {
                'form' : form,
                'order' : order
            }
            return render(request, 'checkout.html', context)
        except ObjectDoesNotExist:
            return redirect('oyeda:checkout')
    
    def post(self, request):
        
        form = CheckoutForm(request.POST)
        
        try:
            order = OrderList.objects.get(user=request.user, ordered=False)
    
            if form.is_valid():
                shipping_address1 = form.cleaned_data.get('shipping_street_address')
                shipping_address2 = form.cleaned_data.get('shipping_street_address_2')
                shipping_city = form.cleaned_data.get('shipping_city')
                shipping_country = form.cleaned_data.get('shipping_country')
                shipping_zip = form.cleaned_data.get('shipping_zip')                
                
                billing_address1 = form.cleaned_data.get('billing_street_address')
                billing_address2 = form.cleaned_data.get('billing_street_address_2')
                billing_city = form.cleaned_data.get('billing_city')
                billing_country = form.cleaned_data.get('billing_country')
                billing_zip = form.cleaned_data.get('billing_zip')
                
                payment_method = form.cleaned_data.get('payment_option')
                
                print(shipping_address1)
                print(shipping_city)
                print(shipping_country)
                print(shipping_zip)

                print(billing_address1)
                print(billing_city)
                print(billing_country)
                print(billing_zip)

                shipping_address = ShippingAddress(
                    user = request.user,
                    street_address = shipping_address1, 
                    apartment_address = shipping_address2, 
                    city = shipping_city, 
                    country = shipping_country,
                    zip = shipping_zip
                )
                
                shipping_address.save()
                
                billing_address = BillingAddress(
                    user = request.user,
                    street_address = billing_address1, 
                    apartment_address = billing_address2, 
                    city = billing_city, 
                    country = billing_country,
                    zip = billing_zip
                )
                
                billing_address.save()

                order.shipping_address = shipping_address
                order.billing_address = billing_address

                order.save() 
                if payment_method == 'S':
                    print('Stripe it is')
                    return redirect('oyeda:payment')
                elif payment_method == 'P':
                    print("PayPal it is my G")
                    return redirect('oyeda:payment')
                else:
                    print('Invalid payment option selected')
                    return redirect('oyeda:home')
        except ObjectDoesNotExist:
            return redirect("oyeda:order-summary")
        
        return render(request, 'checkout.html')

class PaymentView(View):
    def get(self, request):
        order = OrderList.objects.get(user=request.user, ordered=False)
        
        if order.billing_address:
            context = {
                'order' : order,
                'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
            }        
            print('get function works')
            return render(request, 'payment.html', context)
        else:
            print('No billing address input yet')
            return redirect('oyeda:checkout')        

    def post(self, request):
        order = OrderList.objects.get(user=request.user, ordered=False)

        form = PaymentForm(request.POST)
    # alright so apparently while using stripe, you need to use both public and secret keys
    # public one is for creating token, secret one is for charging the token or helping create
    # the charge object
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            print(token)
            amount = int(order.get_total_price())
            print(amount)
            print(stripe.api_key)

            try:
                # problem is here
                charge = stripe.Charge.create(
                    amount=amount,
                    currency="usd",
                    source=token
                )

                print(charge)

                # create payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = request.user
                payment.amount = amount
                payment.save()

                print(payment)
                print(payment.stripe_charge_id)
                print(payment.user)
                print(payment.amount)

                # change ordered status of all items in order to True
                order_items = order.items.all()
                print(order_items)
                for order_item in order_items:
                    order_item.ordered = True
                    print(order_item.ordered)
                    order_item.save()

                # assign payment to order
                order.payment = payment
                order.ordered = True
                order.save()

                print('Order was successful')
                return redirect('oyeda:home')
            
            except stripe.error.CardError as e:
                    body = e.json_body
                    err = body.get('error', {})
                    print('error')
                    # messages.warning(self.request, f"{err.get('message')}")
                    return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                # messages.warning(self.request, "Rate limit error")
                print('error1')
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print('error2')
                # messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                # messages.warning(self.request, "Not authenticated")
                print('error3')
                return redirect("oyeda:payment")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                # messages.warning(self.request, "Network error")
                print('error4')
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                # messages.warning(self.request, "Something went wrong. You were not charged. Please try again.")
                print('error5')
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                # messages.warning(self.request, "A serious error occurred. We have been notifed.")
                print('error6')
                return redirect("oyeda:payment")

        else:
            print("That ain't it G")
    
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

class SearchView(View):
    def get(self, request):
        return render(request, 'search.html')
    
    def post(self, request):
        if request.method == 'POST':
            all_shoes = Shoe.objects.all()
            searched_shoes = request.POST['searchForm']
            shoes = all_shoes.filter(name__contains=searched_shoes)
            print(shoes)
            print(request.POST['searchForm'])
            context = {
                'shoes' : shoes
            }
        return render(request, 'search.html', context)

def products(request):
    context = {
        'shoes' : Shoe.objects.all(),
        'brands' : Brand.objects.all()
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

class BrandView(DetailView):
    model = Brand
    template_name = 'brand.html'

    def get_context_data(self, **kwargs):
        context = super(BrandView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        print(slug)
        context['shoes'] = Shoe.objects.all().filter(brand_slug=slug)
        return context

def new_arrivals(request):
    new_shoes = Shoe.objects.all().filter(new_arrival=True)
    print(new_shoes)
    context = {
        'new_shoes' : new_shoes
    }

    return render(request, 'new_arrivals.html', context)

class ShoeDetailView(DetailView):
    model = Shoe
    template_name = 'individual-product.html'

# LoginRequiredMixin is the class equivalent of @login_required for functions
# class inherits      
class OrderSummary(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'redirect_to'
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
            order = OrderList.objects.get(user=request.user, ordered=False)
            context = {
                'order' : order
            }
            print(order.items.all())
            return render(request, 'order-summary.html', context)

        except ObjectDoesNotExist:
        # ObjectDoesNotExist for all exceptions to get(); used often w try 
        # and except
            # messages.warning(request, 'No orders in the works at the moment.')
            print("Nope...")
            return redirect('/')

def remove_entire_item_from_cart(request, slug):
    item = Shoe.objects.get(slug=slug)
    order_list = OrderList.objects.get(user=request.user, ordered=False)
    order_item = OrderedItem.objects.get(item=item)
    order_list.items.remove(order_item)
    order_item.delete()
    return redirect("oyeda:order-summary")

def remove_from_cart(request, slug):
    try:
        item = Shoe.objects.get(slug=slug)
        order_list = OrderList.objects.get(user=request.user, ordered=False)
        order_item = OrderedItem.objects.get(item=item)
        print(order_list.items)
        print(order_item)
        print(order_item.quantity)
        if order_item.quantity <= 1:
            order_list.items.remove(order_item)
            order_item.delete()
        else:
            order_item.quantity -= 1
            print(order_item.quantity)
            order_item.save()
        return redirect("oyeda:order-summary")
    except OrderedItem.DoesNotExist:
        print("Item hasn't even been ordered yet.")
        return redirect("oyeda:order-summary")
    except OrderList.DoesNotExist:
        print("No order list for you currently brother")
        return redirect("oyeda:order-summary")
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
        order_list.items.add(new_order_item)
        return redirect("oyeda:order-summary")
    except OrderList.DoesNotExist:
        print("No order list for you sir / ma'am")
        new_order = OrderList.objects.create(user=request.user)
        print(new_order)
        order_item = OrderedItem.objects.create(item=item)
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