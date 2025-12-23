from django.urls import path, include
from .views import (
    RegisterView, 
    login, 
    profile, 
    follow,
    unfollow,
)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('register/', RegisterView.as_view()),
    path('login/', login, name= 'login'),
    path('profile/', profile, name='profile'),


    # Source - https://stackoverflow.com/a/58934660
    # Posted by Ignacio Villela, modified by community. See post 'Timeline' for change history
    # Retrieved 2025-12-23, License - CC BY-SA 4.0

    path('follow/<int:user_id>/', follow, name='follow'),
    path('unfollow/<int:user_id>/', unfollow, name='unfollow'),

]
