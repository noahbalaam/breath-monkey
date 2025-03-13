"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Include home app URLs
    path('accounts/', include('allauth.urls')),
    path('wimhof/', include('wimhof.urls')),  # Add WimHof URLs
]