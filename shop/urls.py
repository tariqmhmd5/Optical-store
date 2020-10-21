from django.urls import path, include
from . import views
urlpatterns = [
    # path('', views.products,name='shop'),
    path('men', views.men,name='men'),
    path('women', views.women,name='women'),
    path('cart', views.cart,name='cart'),
    path('checkout', views.checkout,name='checkout'),
    path('myorders', views.my_orders,name='myorders'),
    path('view_product/<int:id>', views.view_product,name='view_product'),
    path('update_item/', views.updateItem,name='update_item'),
    path('processOrder/', views.processOrder,name='processOrder'),
]
