from django.shortcuts import render, HttpResponse
from . models import *

def products(request):
    products = Product.objects.all()
    params = {'product':products}
    return(render(request,'shop/products.html',params))


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        #return(HttpResponse("Nothing in Cart Login to Continue"))
    
    context = {
        'items':items,
        'order':order
    }
    return(render(request,'shop/cart.html',context))

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        #return(HttpResponse("Nothing in Cart Login to Continue"))
    
    context = {
        'items':items,
        'order':order
    }
    return(render(request,'shop/checkout.html',context))

def view_product(request,id):
    prod = Product.objects.filter(id=id)
    context = {
        'product':prod[0]
    }
    return(render(request,'shop/product_view.html',context))
