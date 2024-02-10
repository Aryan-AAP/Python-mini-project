# quiz/models.py
from django.db import models

class QuizItem(models.Model):
    id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)
    subject = models.CharField(max_length=50, default='General')  # Add a default value
