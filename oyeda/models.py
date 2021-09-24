from django.db import models
from django.shortcuts import reverse

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