from django.shortcuts import render
from .models import Book
from rest_framework import generics
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

# Create your views here.
class BookList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    
        