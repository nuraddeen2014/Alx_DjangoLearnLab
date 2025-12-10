from django.shortcuts import render
from django.views.generic.edit import (
    CreateView, 
    UpdateView, 
    DeleteView
    )
from django.views.generic import (
    DetailView,
    ListView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import UserProfile, Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserUpdateForm, ProfileUpdateForm, PostCreationForm


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


@login_required
def profile_update(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'blog/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

#CRUD Operations for Post
class BlogPostListView(ListView):
    template_name = 'blog/home.html'
    model = Post
    context_object_name = 'posts'

class BlogPostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    model = Post
    context_object_name = 'post'


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    fields = ('title', 'content')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        post_pk = self.object.pk
        return reverse_lazy('post-detail', kwargs={'pk': post_pk})

class BlogPostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author