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


from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from .forms import QuizItemForm, BulkImportForm  


from django.shortcuts import render
from .models import QuizItem
import random
from django.shortcuts import render
from .models import QuizItem
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import QuizItem
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import QuizItem
import csv
from io import TextIOWrapper

from .models import QuizItem


from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import QuizItem


from django.shortcuts import render


def index(request):
    if not request.user.is_authenticated:
        
        return render(request, "login.html")
    
    subjects = QuizItem.objects.values("subject").distinct()

    
    user_score = request.session.get("user_score", None)

    return render(request, "index.html", {"subjects": subjects, "user_score": user_score})



def start_quiz(request, subject):
    
    questions = QuizItem.objects.filter(subject=subject)

    
    random_questions = QuizItem.objects.filter(subject=subject).order_by("?")[:10]

    
    context = {
        "subject": subject,
        "all_questions": questions,
        "random_questions": random_questions,
    }

    return render(request, "start_quiz.html", context)


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)

        
        user = authenticate(username=username, password=password)

        if user is not None:
            
            login(request, user)
            return redirect("/")

        else:
            
            return render(request, "login.html")

    return render(request, "login.html")




def logoutUser(request):
    logout(request)
    return redirect("/login")


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def contact(request):

    return render(request, "contact.html")


@staff_member_required
def add_question(request):
    if request.method == "POST":
        if "csv_file" in request.FILES:
            csv_file = request.FILES["csv_file"]
            process_bulk_import(csv_file)
            messages.success(request, "Questions imported successfully!")
            return redirect(reverse("admin:index"))
        else:
            form = QuizItemForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Question added successfully!")
                return redirect(reverse("admin:index"))
    else:
        form = QuizItemForm()

    bulk_import_form = BulkImportForm()
    return render(
        request,
        "add_question.html",
        {"form": form, "bulk_import_form": bulk_import_form},
    )



def process_bulk_import(csv_file):
    
    csv_data = TextIOWrapper(csv_file.file, encoding='utf-8')
    
    csv_reader = csv.reader(csv_data)
    
    header = next(csv_reader, None)
    
    question_text_index = header.index('question_text') if 'question_text' in header else 0
    option1_index = header.index('option1') if 'option1' in header else 1
    option2_index = header.index('option2') if 'option2' in header else 2
    option3_index = header.index('option3') if 'option3' in header else 3
    option4_index = header.index('option4') if 'option4' in header else 4
    correct_option_index = header.index('correct_option') if 'correct_option' in header else 5
    subject_index = header.index('subject') if 'subject' in header else 6

    
    for row in csv_reader:
        
        question_text = row[question_text_index]
        option1 = row[option1_index]
        option2 = row[option2_index]
        option3 = row[option3_index]
        option4 = row[option4_index]
        correct_option = row[correct_option_index]
        subject = row[subject_index]

        
        QuizItem.objects.create(
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            subject=subject,
        )


def submit_quiz(request):
    if request.method == "POST":
        
        user_answers = {}
        for key, value in request.POST.items():
            if key.startswith("question_"):
                question_id = int(key.split("_")[1])
                user_answers[question_id] = value

        
        correct_answers = {}
        questions = QuizItem.objects.all()
        for question in questions:
            correct_answers[question.id] = question.correct_option

        
        score = 0
        for question_id, user_answer in user_answers.items():
            correct_answer = correct_answers.get(question_id, None)
            if correct_answer and user_answer == correct_answer:
                score += 1

        
        request.session["user_score"] = score

        
        return render(request, "quiz_results.html", {"score": score})

    else:
        
        messages.warning(request, "Invalid Access!")
        return redirect("home")  



def Random_Question_start_quiz(request, subject):
    
    questions = QuizItem.objects

    
    random_questions = QuizItem.objects.filter(subject=subject).order_by("?")[:10]

    
    context = {
        "subject": subject,
        "all_questions": questions,
        "random_questions": random_questions,
    }

    return render(request, "start_quiz.html", context)

