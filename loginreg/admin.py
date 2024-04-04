from django.contrib import admin
from .models import QuizItem

# admin.site.register(QuizItem)
from django.contrib import admin
from .models import QuizItem

class QuizItemAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'subject')

# Register your models here.
admin.site.register(QuizItem, QuizItemAdmin)
