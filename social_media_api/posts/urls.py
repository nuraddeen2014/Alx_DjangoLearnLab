from django.urls import path, include
from .views import PostAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostAPIView)
urlpatterns = [
    path('', include(router.urls)),
]
