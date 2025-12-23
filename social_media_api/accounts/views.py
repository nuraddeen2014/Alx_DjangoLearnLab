from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.contrib.auth import get_user_model, authenticate

from rest_framework import(
    generics, 
    permissions,
    response, 
    status, 
    authentication,
    viewsets,
)
from .serializers import (
    CustomUserSerializer,
    RegisterSerializer,
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return response.Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,

            },
            "token": token.key
        })

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated)
    serializer_class = CustomUserSerializer


#Function based views
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful",
            "token": token.key
        }, status=status.HTTP_200_OK)

    return Response({
        "message": "Invalid credentials"
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    # Use the serializer to handle the CustomUser object
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST']) # Best practice: use POST for state changes
@authentication_classes([authentication.TokenAuthentication, authentication.SessionAuthentication])
@permission_classes([permissions.IsAuthenticated])
def follow(request, pk=None):
    # Use get_object_or_404 to prevent server crashes if ID doesn't exist
    target_user = get_object_or_404(User, id=pk)
    
    if request.user == target_user:
        return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    # Logic: "Add this target user to the list of people I am following"
    request.user.followers.add(target_user)
    return Response({'message': f'You are now following {target_user.username}'}, status=status.HTTP_200_OK)

@api_view(['DELETE']) # Best practice: use DELETE for unfollowing
@authentication_classes([authentication.TokenAuthentication, authentication.SessionAuthentication])
@permission_classes([permissions.IsAuthenticated])
def unfollow(request, pk=None):
    target_user = get_object_or_404(User, id=pk)
    
    # Logic: "Remove this target user from the list of people I am following"
    request.user.followers.remove(target_user)
    return Response({'message': f'You have unfollowed {target_user.username}'}, status=status.HTTP_200_OK)

"generics.GenericAPIView", "CustomUser.objects.all()"