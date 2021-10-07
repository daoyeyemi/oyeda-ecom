from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

class Shoe(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=50)
    image = models.ImageField()
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('oyeda:individual-product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('oyeda:add-to-cart', kwargs={
            'slug': self.slug
        })

class OrderedItem(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Item: {self.item.name} - Quantity: {self.quantity}"

class OrderList(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderedItem)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username