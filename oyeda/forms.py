from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
        ('S', 'Stripe'),
        ('P', 'PayPal')
    )

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class CheckoutForm(forms.Form):
    street_address = forms.CharField(required=True)
    street_address_2 = forms.CharField(required=False)
    city = forms.CharField(required=True)
    zip = forms.IntegerField(required=True)
    country = CountryField(blank_label='(Select country)').formfield(
        widget=CountrySelectWidget(attrs={ 'class' : 'country-select' }))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)