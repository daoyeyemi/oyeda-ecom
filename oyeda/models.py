from django.db import models

class Shoe(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=50)
    image = models.ImageField()
    slug = models.SlugField()

    def __str__(self):
        return self.name