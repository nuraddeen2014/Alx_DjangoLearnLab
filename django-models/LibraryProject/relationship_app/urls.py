from . import views
from django.urls import path


urlpatterns = [
    path('book_list/', views.book_list, name='book_list'),
    path('library_detail/<int:pk>', views.LibraryDetailView.as_view()),
]
