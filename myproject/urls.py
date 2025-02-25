from django.contrib import admin
from django.urls import path
from my_app.views import video_feed  # Import your view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('video_feed/', video_feed, name='video_feed'),
]