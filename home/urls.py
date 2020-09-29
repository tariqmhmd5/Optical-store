from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.handleSignup,name='register'),
    path('contact',views.contact,name='contact'),
    path('login',views.handleLogin,name='login'),
    path('logout',views.handleLogout,name='logout'),
]
