from django.urls import path, include
from .views import RegisterView, login, profile


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('register/', RegisterView.as_view()),
    path('login/', login, name= 'login'),
    path('profile/', profile, name='profile'),
]
