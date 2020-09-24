from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.products,name='shop'),
    path('cart', views.cart,name='cart'),
    path('checkout/<int:id>', views.checkout,name='checkout'),
]
