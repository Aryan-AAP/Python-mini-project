from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.urls import reverse
from .forms import QuizItemForm




def index(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect("/login") 
    return render(request, 'index.html')

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")

        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")

def about(request):
    return render(request, 'about.html') 

def services(request):
    return render(request, 'services.html')
 

def contact(request):
   
    return render(request, 'contact.html')
 
 


@staff_member_required
def add_question(request):
    if request.method == 'POST':
        form = QuizItemForm(request.POST)
        if form.is_valid():
            form.save()

            # Redirect to the Django admin panel
            admin_url = reverse('admin:index')
            return redirect(admin_url)
    else:
        form = QuizItemForm()

    return render(request, 'quiz/add_question.html', {'form': form})
