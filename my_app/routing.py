from django.urls import path
from .consumers import VideoFeedConsumer  # Import your WebSocket consumer

websocket_urlpatterns = [
    path("ws/video_feed/", VideoFeedConsumer.as_asgi()),  # WebSocket route
]