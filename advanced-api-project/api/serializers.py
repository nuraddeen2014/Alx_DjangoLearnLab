from .models import Book, Author
from rest_framework import serializers
from datetime import datetime

class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    """ The Author serializer, serializes the author model"""    
    class Meta:
        model = Author
        fields = ['name']

class BookSerializer(serializers.HyperlinkedModelSerializer):
    """The book serializer serializes the book model,
        shows full details of the book's author.
    """

    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
    queryset=Author.objects.all(), source='author', write_only=True
)  

    class Meta:
        model = Book
        fields = ['title','publication_year','author', 'author_id']


    def validate(self,data):
        if data['publication_year'] > datetime.now().year:
            raise serializers.ValidationError('Publication year can not be in the future.')
        return data