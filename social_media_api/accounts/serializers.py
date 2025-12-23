from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()
class CustomUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'followers_count', 'following_count']
        read_only_fields = ['id', 'date_joined']


from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# Small helper serializer to avoid deep recursion when listing users
class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CustomUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    # If you want to see the list of people:
    followers_list = UserBasicSerializer(many=True, source='followers', read_only=True)
    following_list = UserBasicSerializer(many=True, source='following', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'bio', 
            'followers_count', 'following_count',
            'followers_list', 'following_list'
        ]
        read_only_fields = ['id']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        # Accessing the reverse relation defined by related_name='following'
        return obj.following.count()


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

