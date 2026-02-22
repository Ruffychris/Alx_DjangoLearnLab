from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('posts.urls')),  # includes posts, comments, and feed
    path('api/notifications/', include('notifications.urls')),  # social_media_api/urls.py
]

