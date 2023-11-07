from django.contrib.auth.forms import UserCreationForm
from .models import Student, User, Course,Hostel, Complaint
from django import forms

# from django.contrib.auth import get_user_model

# User = get_user_model()



class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': 'same as your roll no.',
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    document=forms.FileField(required=True)
    student_image = forms.ImageField(required=False)
    class Meta:
        model = Student
        fields = [
            'student_name',
            'father_name',
            'enrollment_no',
            'course',
            'dob',
            'gender',
            'document',
            'hostel',
            'student_image',
            'no_dues',
            ]




class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['text']


class SelectionForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['room']

class DuesForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all().filter(no_dues=True))
    amount = forms.DecimalField(max_digits=6, decimal_places=2)

class NoDuesForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all().filter(no_dues=False))
    amount = forms.DecimalField(max_digits=6, decimal_places=2)
    


class DocumentForm(forms.Form):
    docfile=forms.FileField(
        label='select a file'
    )

    
    
    
    
