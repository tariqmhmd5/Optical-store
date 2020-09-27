from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return('Message from: ' + self.name)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.IntegerField()

    def __str__(self):
        return self.user.username
    