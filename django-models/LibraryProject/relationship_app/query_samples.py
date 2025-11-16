import os
import django

# Configure Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import AuthorModel, BookModel, LibraryModel, LibrarianModel

# ------------------------------------------------
# Sample Data Creation
# ------------------------------------------------

author1 = AuthorModel.objects.create(name="Sheikh Ali Fawzan")
author2 = AuthorModel.objects.create(name="Sheikh Abdurrahman Akhdari")

book1 = BookModel.objects.create(title="Explanation of Aqeedah", author=author1)
book2 = BookModel.objects.create(title="Principles of Jurisprudence", author=author1)
book3 = BookModel.objects.create(title="Mukhtasar Al-Akhdari", author=author2)

library1 = LibraryModel.objects.create(name="Central Library")
library1.books.add(book1, book2, book3)

librarian1 = LibrarianModel.objects.create(name="Ahmad Ibrahim", library=library1)

# ------------------------------------------------
# Required Queries
# ------------------------------------------------

print("\n📌 All books by Sheikh Ali Fawzan:")
books_by_fawzan = BookModel.objects.filter(author=author1)
for b in books_by_fawzan:
    print("-", b.title)

print("\n📌 All books in Central Library:")
books_in_library = library1.books.all()
for b in books_in_library:
    print("-", b.title)

print("\n📌 Librarian of Central Library:")
print(library1.librarian.name)
"Library.objects.get(name=library_name)"
x = "Author.objects.get(name=author_name)", "objects.filter(author=author)"
