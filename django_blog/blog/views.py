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
from .models import UserProfile, Post, Comment, Tag
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm, PostCreationForm, CommentForm


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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recent posts for sidebar
        context['recent_posts'] = Post.objects.order_by('-published_date')[:5]
        return context

class BlogPostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-published_date')[:5]
        from .models import Comment
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at')
        return context


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # handle tags
        tags_str = form.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        if tag_names:
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name)
                self.object.tags.add(tag_obj)
        return response

class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostCreationForm

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        post_pk = self.object.pk
        return reverse_lazy('post-detail', kwargs={'pk': post_pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        tags_str = form.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        # set tags (clear current, add new)
        self.object.tags.clear()
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name=name)
            self.object.tags.add(tag_obj)
        return response

class BlogPostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class TagPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return self.tag.posts.order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['recent_posts'] = Post.objects.order_by('-published_date')[:5]
        return context


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return Post.objects.none()
        qs = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['recent_posts'] = Post.objects.order_by('-published_date')[:5]
        return context

#CRUD Operations for Comments
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/create_comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('comment', kwargs={'pk': self.kwargs['pk']})

        

class CommentListView(ListView):
    model = Comment
    template_name = 'blog/comment.html'
    context_object_name = 'comments'

    def get_queryset(self):
        self.post = Post.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(post=self.post).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.post
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'blog/create_comment.html'
    form_class = CommentForm

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        # redirect back to the comments list for this post
        return reverse_lazy('comment', kwargs={'pk': self.object.post.pk})

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this comment.")
        # redirect to the post detail or comments list
        return redirect('post-detail', pk=self.get_object().post.pk)

    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully.')
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete this comment.")
        return redirect('post-detail', pk=self.get_object().post.pk)

    def get_success_url(self):
        return reverse_lazy('comment', kwargs={'pk': self.object.post.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Comment deleted successfully.')
        return super().delete(request, *args, **kwargs)

