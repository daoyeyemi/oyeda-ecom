from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

address_choices = (
    ('B', 'Billing'),
    ('S', 'Shipping')
)

brand_choices = (
    ('Nike', 'Nike'),
    ('Adidas', 'Adidas'),
    ('Puma', 'Puma'),
    ('New Balance', 'New Balance'),
    ('Vans', 'Vans'),
    ('Converse', 'Converse')
)

button_choices = (
    ('primary', 'primary'),
    ('light', 'light'),
    ('danger', 'danger'),
    ('warning', 'warning'),
    ('light', 'light'),
    ('success', 'success')
)

brand_slug_choices = (
    ('nike', 'nike'),
    ('adidas', 'adidas'),
    ('puma', 'puma'),
    ('new-balance', 'new-balance'),
    ('vans', 'vans'),
    ('converse', 'converse')
)

class Brand(models.Model):
    btn_type = models.CharField(choices=button_choices, max_length=20)
    name = models.CharField(choices=brand_choices, max_length=20)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_brand_url(self):
        return reverse('oyeda:brand-selection', kwargs={
            'slug' : self.slug
        })

class Shoe(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    image = models.ImageField()
    slug = models.SlugField()
    new_arrival = models.BooleanField(default=False)
    brand_slug = models.CharField(choices=brand_slug_choices, default='nike', max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('oyeda:individual-product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_slug(self):
        return reverse('oyeda:add-to-cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_slug(self):
        return reverse('oyeda:remove-from-cart', kwargs={
            'slug': self.slug
        })

class OrderedItem(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # setting null attribute to True basically sets empty values as NULL in database
    # null must e set to true
    item = models.ForeignKey(Shoe, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Item: {self.item.name} - Quantity: {self.quantity}"
    
    def generate_total_price_for_item(self):
        quantity = self.quantity
        price = self.item.price
        item_price = quantity * price
        return item_price

class ShippingAddress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField()
    zip = models.IntegerField()
    # address_type = models.CharField(max_length=1, choices=address_choices)

    def __str__(self):
        return f"{self.user.username} - Street Address: {self.street_address}"

class BillingAddress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField()
    zip = models.IntegerField()
    # address_type = models.CharField(max_length=1, choices=address_choices)

    def __str__(self):
        return f"{self.user.username} - Street Address: {self.street_address}"

class Payment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.FloatField()
    stripe_charge_id = models.CharField(max_length=100, default=True)
    # timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

class OrderList(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderedItem, null=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.generate_total_price_for_item()
        return total

    def get_total_items_in_cart(self):
        total_items = 0
        for item in self.items.all():
            total_items += item.quantity
        return total_items
        

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username