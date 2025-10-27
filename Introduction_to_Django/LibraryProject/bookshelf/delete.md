- Book.objects.filter(title='Nineteen Eighty-Four').delete()
(2, {'bookshelf.Book': 2})

- Book.objects.all()
<QuerySet []>

* Empty after Deleted

- ["book.delete", "from bookshelf.models import Book"]