import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from my_app.routing import websocket_urlpatterns  # Import your WebSocket routes

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle HTTP requests
    "websocket": AuthMiddlewareStack(  # Handle WebSocket connections with authentication
        URLRouter(websocket_urlpatterns)  # Use your WebSocket routes
    ),
})