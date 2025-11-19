from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from .models import CustomUser

# Book form for add/edit
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

# Optional custom registration form
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("date_of_birth","profile_photo")
