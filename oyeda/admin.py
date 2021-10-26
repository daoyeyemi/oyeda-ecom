from django.contrib import admin
from .models import Shoe, OrderedItem, OrderList, BillingAddress, ShippingAddress, Payment

admin.site.register(Shoe)
admin.site.register(OrderedItem)
admin.site.register(OrderList)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(Payment)