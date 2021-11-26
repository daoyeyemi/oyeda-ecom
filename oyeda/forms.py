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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})

class CheckoutForm(forms.Form):
    shipping_street_address = forms.CharField(required=True)
    shipping_street_address_2 = forms.CharField(required=False)
    shipping_city = forms.CharField(required=True)
    shipping_zip = forms.IntegerField(required=True)
    shipping_country = CountryField(blank_label='(Select country)').formfield(
        widget=CountrySelectWidget(attrs={ 'class' : 'country-select' }))
    billing_street_address = forms.CharField(required=True)
    billing_street_address_2 = forms.CharField(required=False)
    billing_city = forms.CharField(required=True)
    billing_zip = forms.IntegerField(required=True)
    billing_country = CountryField(blank_label='(Select country)').formfield(
        widget=CountrySelectWidget(attrs={ 'class' : 'country-select' }))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=True)