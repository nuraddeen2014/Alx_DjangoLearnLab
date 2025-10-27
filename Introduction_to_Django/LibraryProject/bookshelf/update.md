- Book.objects.filter(title='1984').update(title='Nineteen Eighty-Four')

- Output : Book.objects.filter(title='Nineteen Eighty-Four')
<QuerySet [(Nineteen 
Eighty-Four, George Orwell, 1949), (Nineteen Eighty-Four, George Orwell, 1949)]>

- ["book.title"] is empty