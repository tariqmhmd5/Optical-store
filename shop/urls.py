from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.products,name='shop'),
    path('cart', views.cart,name='cart'),
    path('checkout', views.checkout,name='checkout'),
    path('view_product/<int:id>', views.view_product,name='view_product'),
]
