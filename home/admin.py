from django.contrib import admin
from . models import Contact
from . models import UserProfile

admin.site.register(Contact)
admin.site.register(UserProfile)

