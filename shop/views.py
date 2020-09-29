from django.shortcuts import render
from .models import Product
from math import ceil

def products(request):
    products = Product.objects.all()
    n= len(products)
    params = {'product':products}
    return(render(request,'shop/products.html',params))


def cart(request):
    return(render(request,'shop/cart.html'))

def checkout(request):
    return(render(request,'shop/checkout.html'))

def view_product(request,id):
    prod = Product.objects.filter(id=id)
    context = {
        'product':prod[0]
    }
    return(render(request,'shop/product_view.html',context))
