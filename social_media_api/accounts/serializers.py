from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'bio', 'profile_picture']
        read_only_fields = ['id', 'date_joined']

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  # hashed automatically
        )
        return user
    #Token.objects.create() implemented in views