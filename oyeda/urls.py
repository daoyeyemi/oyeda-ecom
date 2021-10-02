from django.urls import path, include
from . import views

app_name = 'oyeda'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<slug>/', views.ShoeDetailView.as_view(), name='individual-product'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-summary/', views.OrderSummary.as_view(), name='order-summary')
]