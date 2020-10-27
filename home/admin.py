from django.contrib import admin
from . models import Contact
from . models import Appointment

admin.site.register(Contact)
admin.site.register(Appointment)

