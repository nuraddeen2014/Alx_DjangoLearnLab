from django.urls import path
from django.views import generic
from .views import SignUpView, CustomLoginView, ProfileDetailView, ProfileUpdateView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', generic.TemplateView.as_view(template_name='blog/home.html'), name='home'),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/', ProfileDetailView.as_view(), name='profile'),
    path('accounts/profile/edit', ProfileUpdateView.as_view(), name='profile-edit'),
]
