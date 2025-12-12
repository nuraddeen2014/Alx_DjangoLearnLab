from django.contrib import admin
from .models import Post, UserProfile, Comment, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'published_date')
	search_fields = ('title', 'content')
	list_filter = ('published_date', 'author')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('post', 'author', 'created_at')
	search_fields = ('content',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	search_fields = ('name',)
