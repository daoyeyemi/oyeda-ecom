from django.contrib import admin
from .models import Brand, Shoe, OrderedItem, OrderList, BillingAddress, ShippingAddress, Brand, Payment, SubscriberEmail

admin.site.register(Shoe)
admin.site.register(OrderedItem)
admin.site.register(OrderList)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Brand)
admin.site.register(SubscriberEmail)