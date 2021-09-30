from django.contrib import admin
from .models import Shoe, OrderedItem, OrderList

admin.site.register(Shoe)
admin.site.register(OrderedItem)
admin.site.register(OrderList)