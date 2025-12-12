from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile, Post, Comment

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email Address', required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_photo')

class PostCreationForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text='Comma-separated tags', widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2'}))

    class Meta:
        model = Post
        fields = ('title', 'content', )

    def __init__(self, *args, **kwargs):
        # allow initializing tags string when editing
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance and instance.pk:
            self.fields['tags'].initial = ', '.join([t.name for t in instance.tags.all()])

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


        #TagWidget()", "widgets"