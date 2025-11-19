from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Library,Cars
from django.views.generic import DetailView,ListView,UpdateView
from .forms import BookForm, RegisterForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin


# Role check functions
def is_admin(user):
    return user.userprofile.role == "ADMIN"

def is_librarian(user):
    return user.userprofile.role == "LIBRARIAN"

def is_member(user):
    return user.userprofile.role == "MEMBER"

# Book list
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {'books': books})

# Library detail CBV
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'bookshelf/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.get_object().books.all()
        return context

# User registration
class Register(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'bookshelf/register.html'

# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    return render(request,'bookshelf/admin_view.html', {'profile': request.user.userprofile})

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request,'bookshelf/librarian_view.html', {'profile': request.user.userprofile})

@user_passes_test(is_member)
def member_view(request):
    return render(request,'bookshelfmember_view.html', {'profile': request.user.userprofile})

# Book CRUD FBVs with permissions
@permission_required('bookshelf.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

@permission_required('bookshelf.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})


class CarListView(PermissionRequiredMixin,ListView):
    model = Cars
    template_name = 'bookshelf/cars.html'
    context_object_name = 'cars'
    permission_required = 'bookshelf.can_view_cars'

class CarUpdateView(PermissionRequiredMixin, UpdateView):
    model = Cars
    fields = ['name']
    template_name = 'bookshelf/cars_update.html'
    success_url = reverse_lazy('cars')
    permission_required = 'bookshelf.cars_update.html'