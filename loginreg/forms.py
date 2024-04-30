# # quiz/forms.py
# from django import forms
# from .models import QuizItem

# class QuizItemForm(forms.ModelForm):
#     class Meta:
#         model = QuizItem
#         fields = ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option', 'subject']

#     def __init__(self, *args, **kwargs):
#         super(QuizItemForm, self).__init__(*args, **kwargs)
#         # You can customize the appearance of the form fields here, if needed
# from loginreg.forms import UserDataForm


# quiz/forms.py
from django import forms
from .models import QuizItem

class QuizItemForm(forms.ModelForm):
    class Meta:
        model = QuizItem
        fields = ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option', 'subject']

class BulkImportForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')

