from django.urls import path
from django.views import generic
from django.contrib.auth.views import LogoutView
from .views import (

    #Auth and profile management
    SignUpView, 
    CustomLoginView, 
    profile_update, 
    ProfileDetailView,
    #BlogPost Crud operations
    BlogPostCreateView,
    BlogPostListView,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostDelete,
    #Post Comments CRUD
    PostCommentView,
    PostCommentCreateView,

    )


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
    path('post/new/', BlogPostCreateView.as_view(), name='create-post'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', BlogPostUpdateView.as_view(), name='update-post'),
    path('post/<int:pk>/delete/', BlogPostDelete.as_view(), name='delete-post'),

    #comment CRUD
    path('post/<int:pk>/comment/', PostCommentView.as_view(), name='comment'),
    path('post/<int:pk>/comment/create/', PostCommentCreateView.as_view(), name='create-comment')
]
