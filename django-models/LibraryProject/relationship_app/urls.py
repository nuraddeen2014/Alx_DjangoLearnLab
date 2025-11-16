from . import views
from .views import SignUpView
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('book_list/', views.book_list, name='book_list'),
    path('library_detail/<int:pk>', views.LibraryDetailView.as_view()),
]
