from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Book CRUD
    path('add_book/', views.add_book, name='add_book'),
    path('<int:pk>/edit_book/', views.edit_book, name='edit_book'),
    path('<int:pk>/delete_book/', views.delete_book, name='delete_book'),

    # Role-based dashboards
    path('admin_view/', views.admin_view, name='admin_view'),
    path('librarian_view/', views.librarian_view, name='librarian_view'),
    path('member_view/', views.member_view, name='member_view'),

    # Registration & login/logout
    path('register/', views.Register.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='bookshelf/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='bookshelf/logout.html'), name='logout'),

    # Book/List Views
    path('book_list/', views.book_list, name='book_list'),
    path('library_detail/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    #Cars
    path('cars/', views.CarListView.as_view(), name='cars'),
    path('cars_update/<int:pk>/', views.CarUpdateView.as_view(), name='cars_update')
]
