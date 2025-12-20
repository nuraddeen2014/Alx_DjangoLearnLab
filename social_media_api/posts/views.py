from django.shortcuts import render
from rest_framework import generics, viewsets
from .permissions import OnlyOwnerDeletesPermission

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
    permission_classes = [OnlyOwnerDeletesPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentAPIView(viewsets.ModelViewSet):
    permission_classes = [OnlyOwnerDeletesPermission]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

