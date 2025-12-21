from django.urls import path, include
from .views import PostAPIView, CommentAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostAPIView)
router.register(r'comments', CommentAPIView)


urlpatterns = [
    path('', include(router.urls)),
]
