from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.urls import reverse
from .forms import QuizItemForm
from .models import QuizItem



# views.py
from django.shortcuts import render
from .models import QuizItem
import random

def index(request):
    if request.user.is_anonymous:
        return redirect("/login") 

    # Fetch unique subjects from the database
    subjects = QuizItem.objects.values('subject').distinct()

    return render(request, 'index.html', {'subjects': subjects})

from django.shortcuts import render
from .models import QuizItem

def start_quiz(request, subject):
    # Retrieve questions for the given subject
    questions = QuizItem.objects.filter(subject=subject)

    # Fetch random 10 questions for the selected subject
    random_questions = QuizItem.objects.filter(subject=subject).order_by('?')[:10]

    # Pass the questions and options as context to the template
    context = {
        'subject': subject,
        'all_questions': questions,
        'random_questions': random_questions,
    }

    return render(request, 'start_quiz.html', context)


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

    return render(request, 'add_question.html', {'form': form})


# views.py
from django.shortcuts import render

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import QuizItem

       
from django.shortcuts import render

# def quiz_results(request):
#     # Your logic to calculate quiz results and pass data to the template
#     total_questions = 10  # Replace with the actual total number of questions
#     correct_answers = 7  # Replace with the actual number of correct answers
#     incorrect_answers = total_questions - correct_answers
#     percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

#     context = {
#         'total_questions': total_questions,
#         'correct_answers': correct_answers,
#         'incorrect_answers': incorrect_answers,
#         'percentage': percentage,
#     }

#     return render(request, 'quiz_results.html', context)

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import QuizItem

def submit_quiz(request):
    if request.method == 'POST':
        # Retrieve user-submitted answers from the form
        user_answers = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                user_answers[question_id] = value

        # Retrieve correct answers from the database
        correct_answers = {}
        questions = QuizItem.objects.all()
        for question in questions:
            correct_answers[question.id] = question.correct_option

        # Compare user answers with correct answers and calculate the score
        score = 0
        for question_id, user_answer in user_answers.items():
            correct_answer = correct_answers.get(question_id, None)
            if correct_answer and user_answer == correct_answer:
                score += 1

        # Pass the score to the template
        return render(request, 'quiz_results.html', {'score': score})

    else:
        # If someone tries to access the submit_quiz page directly without submitting the form
        messages.warning(request, 'Invalid Access!')
        return redirect('home')  # Redirect to the home page or any other page


