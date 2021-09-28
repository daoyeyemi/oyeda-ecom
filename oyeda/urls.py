from django.urls import path, include
from . import views

app_name = 'oyeda'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<slug>/', views.ShoeDetailView.as_view(), name='individual-product'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup')
]