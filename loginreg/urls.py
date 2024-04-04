from django.contrib import admin
from django.urls import path, include
from loginreg import views
from django.urls import path

from . import views


from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("start_quiz/<str:subject>/", views.start_quiz, name="start_quiz"),
    path("submit_quiz/", views.submit_quiz, name="submit_quiz"),
    path("login", views.loginUser, name="login"), 
    path("logout/", views.logoutUser, name="logout"),  
    path("about", views.about, name="about"),
    path("services", views.services, name="services"),
    path("contact", views.contact, name="contact"),
    path("add_question/", views.add_question, name="add_question"),
    path("submit_quiz/", views.submit_quiz, name="submit_quiz"),
]


# from django.urls import path, include
# from loginreg import views

# urlpatterns = [
#     path('', views.index, name="home"),
#     path('start_quiz/<str:subject>/', views.start_quiz, name='start_quiz'),
#     path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
#     path('login/', views.loginUser, name="login"),  # Updated login URL pattern
#     path('logout/', views.logoutUser, name="logout"),
#     path("about/", views.about, name='about'),
#     path("services/", views.services, name='services'),
#     path("contact/", views.contact, name='contact'),
#     path('add_question/', views.add_question, name='add_question'),
#     path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
# ]
