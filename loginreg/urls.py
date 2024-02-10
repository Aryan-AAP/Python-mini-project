from django.contrib import admin
from django.urls import path, include
from loginreg import views
from django.urls import path
from . import views

# Your URL patterns go here

urlpatterns = [ 
    path('',views.index, name="home"),
    
    path('login',views.loginUser, name="login"),
    path('logout',views.logoutUser, name="logout"),
        path("about", views.about, name='about'),
    path("services", views.services, name='services'),
    path("contact", views.contact, name='contact'), 
    path('add_question/', views.add_question, name='add_question'),

]