from django.shortcuts import render, HttpResponse
from . models import *
from django.http import JsonResponse
import json
import datetime

def men(request):
    products = Product.objects.filter(category="Men Eyewear")

    if request.user.is_authenticated:   
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        cartItems = order['get_cart_items']
        #return(HttpResponse("Nothing in Cart Login to Continue"))
    

    params = {'product':products, 'cartItems':cartItems}
    return(render(request,'shop/products.html',params))


def women(request):
    products = Product.objects.filter(category="Women Eyewear")

    if request.user.is_authenticated:   
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        cartItems = order['get_cart_items']
        #return(HttpResponse("Nothing in Cart Login to Continue"))
    

    params = {'product':products, 'cartItems':cartItems}
    return(render(request,'shop/products.html',params))


def cart(request):
    if request.user.is_authenticated:   
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        cartItems = order['get_cart_items']
        #return(HttpResponse("Nothing in Cart Login to Continue"))
    
    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return(render(request,'shop/cart.html',context))

def my_orders(request):
    print('inside')
    if request.user.is_authenticated:   
        customer = request.user.customer
        
        order = Order.objects.filter(customer=customer,complete=True)
        items = [OrderItem.objects.filter(order=i) for i in order]
        ordered = []
        for item_list in items:
            for item in item_list:
                ordered.append(item)
        #items = order.orderitem_set.all()
        #cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        cartItems = order['get_cart_items']
        #return(HttpResponse("Nothing in Cart Login to Continue"))
    
    context = {
        #'items':items,
        'items': ordered
        #'cartItems':cartItems
    }
    return(render(request,'shop/my_orders.html',context))

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        cartItems = order['get_cart_items']
        #return(HttpResponse("Nothing in Cart Login to Continue"))
    
    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return(render(request,'shop/checkout.html',context))

def view_product(request,id):
    if request.user.is_authenticated:   
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        cartItems = order.get_cart_items
    prod = Product.objects.filter(id=id)
    context = {
        'product':prod[0],
        'cartItems':cartItems
    }
    return(render(request,'shop/product_view.html',context))

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer 
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) 

    if action=='add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse("Item was added in theeeeee carrtt", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete =True
        order.save()

        ShippingAddress.objects.create(
            customer = customer,
            order=order,
            name= data['form']['name'],
            email= data['form']['email'],
            phone= data['form']['phone'],
            address= data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )


    return JsonResponse("Payment Complete",safe=False)
