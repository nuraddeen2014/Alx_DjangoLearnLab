from django.db import models

# Create your models here.
class Author(models.Model):
    # This creates an author model
    name = models.CharField(max_length=50)

class Book(models.Model):
    """The book model maps every instance
        of a book to a specific author.
    """

    title = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title