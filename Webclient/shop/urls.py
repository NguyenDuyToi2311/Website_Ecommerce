from django import views
from django.urls import path
from . import views
from . models import *


urlpatterns = [
    path('', views.main, name='main'),
    
    path('register/', views.register, name = 'register'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    
    path('collection/', views.collection, name = 'collection'),
    path('collection/<str:name>/',views.collectionview,name = "collection"),
    path('collection/<str:cname>/<str:pname>/',views.product_detail,name = "product_detail"),
    
    path('addtocart/', views.add_to_cart, name = 'addtocart'),
    path('cart/', views.cart, name = 'cart'),
    path('removecart/<str:id>', views.remove_cart, name = 'removecart'),
    
    path('checkout/', views.check_out, name = 'checkout'),
    
]
