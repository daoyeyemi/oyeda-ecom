from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# from django_countries import CountryField

PAYMENT_CHOICES = (
        ('S', 'Stripe'),
        ('P', 'PayPal')
    )

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    street_address_2 = forms.CharField(required=False)
    city = forms.CharField()
    zip = forms.IntegerField()
    # country = CountryField(blank_label='(Select country)')
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


    

