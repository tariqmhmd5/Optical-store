from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . models import Contact
from . models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from shop.models import *

def home(request):
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
        'cartItems':cartItems
    }

    return(render(request,'home/home.html',context))

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contact(name=name,email=email,subject=subject,message=message)
        contact.save()
        messages.success(request,"Message Sent!")

        return(render(request,'home/home.html'))
        
    else:
        return(HttpResponse("404 Not found"))
    

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        c_password = request.POST['c_password']

        if password==c_password:
            try:
                myuser = User.objects.create_user(username,email,password)
                name= fname.split(" ")
                myuser.first_name = name[0]
                myuser.last_name = name[-1]
                myuser.save()
                user = User.objects.get(username=username)
                profile = UserProfile(user=user,phone=phone)
                profile.save()
                
                customer = Customer(user=user,name=fname,email=email)
                customer.save()

                messages.success(request,"Your account is created sucessfully")
                return(redirect('home'))
            except Exception as e:
                messages.warning(request,"User already registered. Try Login.")
                return(redirect('home'))
            
        else:
            messages.error(request,"Password did not match. Try Again")
            return(redirect('home'))
    else:
        return(HttpResponse('404 Not Found'))



def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['username']
        loginpass = request.POST['password']

        loginuser = authenticate(username= loginusername,password= loginpass)

        if loginuser is not None:
            login(request,loginuser)
            messages.success(request, "Sucessfully Logged In")
            return(redirect('home'))
        else:
            messages.error(request, "Invalid username or password")
            return(redirect('home'))
            
    return(HttpResponse("404 Not Found"))


def handleLogout(request):
    logout(request)
    messages.success(request,"Logged out Sucessfully")
    return(redirect('home'))
