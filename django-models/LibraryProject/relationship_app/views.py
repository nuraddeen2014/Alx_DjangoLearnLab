from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.userprofile.role == "ADMIN"
def is_librarian(user):
    return user.userprofile.role == "LIBRARIAN"
def is_member(user):
    return user.userprofile.role == "MEMBER"

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    context = {'books':books}

    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.get_object().books.all()
        return context

class register(CreateView):
    form_class = UserCreationForm()
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'


@user_passes_test(is_admin)
def admin_view(request):
    profile = request.user.userprofile
    context = {'profile':profile}

    return render(request,'admin_view.html', context)


@user_passes_test(is_librarian)
def librarian_view(request):
    profile = request.user.userprofile
    context = {'profile':profile}

    return render(request,'librarian_view.html', context)


@user_passes_test(is_member)
def member_view(request):
    profile = request.user.userprofile
    context = {'profile':profile}

    return render(request,'member_view.html', context)


"relationship_app/member_view.html", "relationship_app/librarian_view.html", "relationship_app/admin_view.html