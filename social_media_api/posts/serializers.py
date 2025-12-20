from rest_framework import serializers
from posts.models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comment = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title','content', 'created_at', 'updated_at', 'comment']