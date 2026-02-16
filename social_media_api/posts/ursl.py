from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PostViewSet, CommentViewSet, feed_view

# Router for Post and Comment CRUD
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls

# Feed endpoint
urlpatterns += [
    path('feed/', feed_view, name='feed'),
]
