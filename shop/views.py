from django.shortcuts import render, HttpResponse
from . models import *
from django.http import JsonResponse
import json
from django.contrib import messages
import datetime

def men(request):
    products = Product.objects.filter(category="Men Eyewear")

    if request.user.is_authenticated:   
        user = request.user
        order, created = Order.objects.get_or_create(user=user,complete=False)
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
        user = request.user
        order, created = Order.objects.get_or_create(user=user,complete=False)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        cartItems = order['get_cart_items']
        #return(HttpResponse("Nothing in Cart Login to Continue"))
    

    params = {'product':products, 'cartItems':cartItems}
    return(render(request,'shop/products.html',params))

def search(request):
    if request.user.is_authenticated:   
        user = request.user
        order, created = Order.objects.get_or_create(user=user,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items   
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        cartItems = order['get_cart_items']

    query = request.POST['query']
    if len(query)>78:
        allsearch = Product.objects.none()
    else:
        name = Product.objects.filter(product_name__icontains=query)
        desc = Product.objects.filter(desc__icontains=query)
        allsearch = name.union(desc)
        
    
    context = {
            'allsearch': allsearch,
            'query': query,
            'cartItems':cartItems
        }

    if allsearch.count() == 0:
        messages.warning(request,"No Search results")
    
    return(render(request,'shop/search.html',context))

def cart(request):
    if request.user.is_authenticated:   
        user = request.user
        order, created = Order.objects.get_or_create(user=user,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        if cartItems==0:
            messages.warning(request,"Cart is Empty!")
            return(render(request,'shop/cart.html'))
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        cartItems = order['get_cart_items']
        messages.warning(request,"Login to Continue")
        return(render(request,'home/home.html'))
    
    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return(render(request,'shop/cart.html',context))

def my_orders(request):
    if request.user.is_authenticated:   
        user = request.user
        
        order = Order.objects.filter(user=user,complete=True)
        items = [OrderItem.objects.filter(order=i) for i in order]
        ordered = []
        for item_list in items:
            for item in item_list:
                ordered.append(item)
        #items = order.orderitem_set.all()
        #cartItems = order.get_cart_items
        if len(ordered)==0:
            messages.warning(request,"Buy Something...")
    else:
        messages.warning(request,'Login to view Myorders.')
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
        user = request.user
        order, created = Order.objects.get_or_create(user=user,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        if cartItems==0:
            messages.warning(request,"Cart is Empty!")
            return(render(request,'shop/cart.html'))
    else:
        items = []
        order = {'get_cart_total':0,"get_cart_items":0}
        cartItems = order['get_cart_items']
        messages.warning(request,"Login to Continue")
        return(render(request,'home/home.html'))
    
    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return(render(request,'shop/checkout.html',context))

def view_product(request,id):
    if request.user.is_authenticated:   
        user = request.user
        order, created = Order.objects.get_or_create(user=user,complete=False)
        cartItems = order.get_cart_items
        prod = Product.objects.filter(id=id)
        context = {
        'product':prod[0],
        'cartItems':cartItems
        }
    else:
        prod = Product.objects.filter(id=id)
        context = {
        'product':prod[0],
        }

    return(render(request,'shop/product_view.html',context))

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    user = request.user
    
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=user,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) 

    if action=='add':
        orderItem.quantity = (orderItem.quantity+1)
        messages.success(request,"Added to cart")
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
        user = request.user
        
        order, created = Order.objects.get_or_create(user=user,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete =True
        order.save()

        ShippingAddress.objects.create(
            user = user,
            order=order,
            name= data['form']['name'],
            email= data['form']['email'],
            phone= data['form']['phone'],
            address= data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
        messages.success(request,"Order Placed")


    return JsonResponse("Payment Complete",safe=False)
