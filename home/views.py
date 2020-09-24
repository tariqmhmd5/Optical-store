from django.shortcuts import render
from . models import Contact

def home(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contact(name=name,email=email,subject=subject,message=message)
        contact.save()


    return(render(request,'home/home.html'))
