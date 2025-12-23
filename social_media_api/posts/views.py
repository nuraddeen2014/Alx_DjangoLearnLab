from django.shortcuts import render
from rest_framework import generics, viewsets
from .permissions import OnlyOwnerDeletesPermission
from django.contrib.auth import get_user_model
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

User = get_user_model()
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

class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, OnlyOwnerDeletesPermission]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        # Fetch posts where the author is someone the current user follows
        # select_related('author') avoids N+1 queries for the author's details
        return Post.objects.filter(
            author__in=user.following.all()
        ).select_related('author')