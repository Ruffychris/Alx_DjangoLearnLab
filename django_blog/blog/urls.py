from django.urls import path

from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,

    user_login,
    user_logout,
    register,
    profile,
)


urlpatterns = [

    # Auth
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

    # Posts
    path('posts/', PostListView.as_view(), name='post-list'),

    path('posts/new/', PostCreateView.as_view(), name='post-create'),

    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),

    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
