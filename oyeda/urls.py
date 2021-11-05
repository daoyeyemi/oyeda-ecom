from django.urls import path, include
from . import views

app_name = 'oyeda'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    # path('brand/', views.brand, name='brand'),
    path('products/<brand>/', views.BrandView.as_view(), name='brand-selection'),
    path('products/<slug>/', views.ShoeDetailView.as_view(), name='individual-product'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-summary/', views.OrderSummary.as_view(), name='order-summary'),
    path('logout/', views.user_logout, name='user_logout'),
    path('add-to-cart/<slug>/', views.add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name="remove-from-cart"),
    path('remove-entire-item-from-cart/<slug>/', views.remove_entire_item_from_cart, name="remove-entire-item"),
    path('payment/', views.PaymentView.as_view(), name="payment"),
    path('search/', views.SearchView.as_view(), name='search')
]