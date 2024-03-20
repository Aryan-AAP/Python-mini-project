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
from .forms import QuizItemForm, BulkImportForm  # Make sure to import BulkImportForm

# views.py
from django.shortcuts import render
from .models import QuizItem
import random
from django.shortcuts import render
from .models import QuizItem
from django.contrib.auth.decorators import login_required

# @login_requiredfrom django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def index(request):
    if not request.user.is_authenticated:
        # return redirect(reverse('login')) 
        return render(request, "login.html")
        # If user is not authenticated, redirect them to the login page
        #  # Assuming the login URL name is 'login'

    # Fetch unique subjects from the database
    subjects = QuizItem.objects.values("subject").distinct()

    # Check if the user has a score stored in the session
    user_score = request.session.get("user_score", None)

    return render(request, "index.html", {"subjects": subjects, "user_score": user_score})



def start_quiz(request, subject):
    # Retrieve questions for the given subject
    questions = QuizItem.objects.filter(subject=subject)

    # Fetch random 10 questions for the selected subject
    random_questions = QuizItem.objects.filter(subject=subject).order_by("?")[:10]

    # Pass the questions and options as context to the template
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

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")

        else:
            # No backend authenticated the credentials
            return render(request, "login.html")

    return render(request, "login.html")


# from django.shortcuts import render, redirect
# from django.contrib.auth import logout, authenticate, login
# from django.contrib.auth.models import User

# def loginUser(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         print(username, password)

#         # check if user has entered correct credentials
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             # A backend authenticated the credentials
#             login(request, user)
#             return redirect("/")  # Redirect to the homepage after successful login

#         else:
#             # No backend authenticated the credentials
#             return render(request, "login.html")

#     return render(request, "login.html")


def logoutUser(request):
    logout(request)
    return redirect("/login")


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def contact(request):

    return render(request, "contact.html")


# @staff_member_required
# quiz/views.py
from django.http import HttpResponseRedirect
from django.urls import reverse


@staff_member_required
def add_question(request):
    if request.method == "POST":
        # Check if it's a regular form submission or a bulk import
        if "csv_file" in request.FILES:
            # Handle bulk import
            csv_file = request.FILES["csv_file"]
            # Process the CSV file and add questions to the database
            process_bulk_import(csv_file)
            messages.success(request, "Questions imported successfully!")
            return redirect(reverse("admin:index"))
        else:
            # Handle regular form submission
            form = QuizItemForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Question added successfully!")
                return redirect(reverse("admin:index"))
    else:
        form = QuizItemForm()

    # Render the form for regular question addition
    bulk_import_form = BulkImportForm()
    return render(
        request,
        "add_question.html",
        {"form": form, "bulk_import_form": bulk_import_form},
    )


import csv
from io import TextIOWrapper

from .models import QuizItem

def process_bulk_import(csv_file):
    # Ensure the CSV file is opened in text mode with utf-8 encoding
    csv_data = TextIOWrapper(csv_file.file, encoding='utf-8')

    # Create a CSV reader
    csv_reader = csv.reader(csv_data)

    # Skip the header row if it exists
    header = next(csv_reader, None)

    # Define the column indices based on the header or order
    question_text_index = header.index('question_text') if 'question_text' in header else 0
    option1_index = header.index('option1') if 'option1' in header else 1
    option2_index = header.index('option2') if 'option2' in header else 2
    option3_index = header.index('option3') if 'option3' in header else 3
    option4_index = header.index('option4') if 'option4' in header else 4
    correct_option_index = header.index('correct_option') if 'correct_option' in header else 5
    subject_index = header.index('subject') if 'subject' in header else 6

    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Extract data from the row
        question_text = row[question_text_index]
        option1 = row[option1_index]
        option2 = row[option2_index]
        option3 = row[option3_index]
        option4 = row[option4_index]
        correct_option = row[correct_option_index]
        subject = row[subject_index]

        # Create a QuizItem object and save it to the database
        QuizItem.objects.create(
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            subject=subject,
        )

# Now you can call this function in your 'add_question' view when handling the bulk import submission.


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
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import QuizItem

def submit_quiz(request):
    if request.method == "POST":
        # Retrieve user-submitted answers from the form
        user_answers = {}
        for key, value in request.POST.items():
            if key.startswith("question_"):
                question_id = int(key.split("_")[1])
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

        # Store the user's score in the session
        request.session["user_score"] = score

        # Pass the score to the template
        return render(request, "quiz_results.html", {"score": score})

    else:
        # If someone tries to access the submit_quiz page directly without submitting the form
        messages.warning(request, "Invalid Access!")
        return redirect("home")  # Redirect to the home page or any other page
