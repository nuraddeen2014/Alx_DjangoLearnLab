from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import UserProfile


User = get_user_model()
# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    success_url = reverse_lazy('home')

#Profile details
class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'blog/profile.html'
    model = UserProfile
    context_object_name = 'profile'
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileUpdateForm
    template_name = 'blog/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile
