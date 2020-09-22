from django.shortcuts import render
from .models import Product
from math import ceil

def products(request):
    products = Product.objects.all()
    n= len(products)
    params = {'product':products}
    return(render(request,'shop/products.html',params))
