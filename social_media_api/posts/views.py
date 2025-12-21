from django.shortcuts import render
from rest_framework import generics, viewsets
from .permissions import OnlyOwnerDeletesPermission
from rest_framework.permissions import (
    IsAuthenticated,
    
)
from rest_framework.authentication import (
    TokenAuthentication, 
    SessionAuthentication,
)

from .models import (
    Post,
    Comment,
)
from .serializers import (
    PostSerializer,
    CommentSerializer,
)

# Create your views here.
class PostAPIView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, OnlyOwnerDeletesPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentAPIView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, OnlyOwnerDeletesPermission]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

