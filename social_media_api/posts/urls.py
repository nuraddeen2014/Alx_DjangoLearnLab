from django.urls import path, include
from .views import PostAPIView, CommentAPIView, FeedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostAPIView)
router.register(r'comments', CommentAPIView)


urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedViewSet.as_view({'get':'list'})),
]
