from django.contrib import admin
from django.urls import path, include  # must include 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # include the app urls
]
