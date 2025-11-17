from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Book form for add/edit
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

# Optional custom registration form
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
