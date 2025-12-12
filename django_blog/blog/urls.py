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
    CommentListView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView
    ,TagPostListView, SearchResultsView

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

    #comment CRUD post/<int:pk>/comments/new/
    path('post/<int:pk>/comment/', CommentListView.as_view(), name='comment'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='create-comment'),
    # comment update uses comment's pk directly
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('tags/<slug:slug>/', TagPostListView.as_view(), name='posts-by-tag'),
    path('search/', SearchResultsView.as_view(), name='search'),
]


#tags/<slug:tag_slug>/", "PostByTagListView.as_view()