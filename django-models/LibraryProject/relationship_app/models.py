from django.db import models

# Create your models here.
class AuthorModel(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class BookModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class LibraryModel(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(BookModel)

class LibrarianModel(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(LibraryModel, on_delete=models.CASCADE)
