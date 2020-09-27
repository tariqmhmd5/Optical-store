from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . models import Contact
from . models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def home(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contact(name=name,email=email,subject=subject,message=message)
        contact.save()

        messages.success(request,"Message Sent!")


    return(render(request,'home/home.html'))

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        c_password = request.POST['c_password']

        if password==c_password:
            myuser = User.objects.create_user(username,email,password)
            name= fname.split(" ")
            myuser.first_name = name[0]
            myuser.last_name = name[-1]
            myuser.save()
            user = User.objects.get(username=username)
            profile = UserProfile(user=user,phone=phone)
            profile.save()
            messages.success(request,"Your account is created sucessfully")
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
