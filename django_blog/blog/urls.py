from django.urls import path
from django.views import generic
from .views import (
    SignUpView, 
    CustomLoginView, 
    profile_update, 
    ProfileDetailView,
    BlogPostCreateView,
    BlogPostListView,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostDelete,
    )
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', BlogPostListView.as_view(), name='home'),

    #Auth and register
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    #profile management
    path('accounts/profile/', ProfileDetailView.as_view(), name='profile'),
    path('accounts/profile/edit', profile_update, name='profile-edit'),

    #Post CRUD
    path('post/create/', BlogPostCreateView.as_view(), name='create-post'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='update-post'),
    path('post/<int:pk>/delete/', BlogPostDelete.as_view(), name='delete-post'),
]
