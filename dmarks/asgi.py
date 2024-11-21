"""
ASGI config for dmarks project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
app = get_asgi_application()

import os
import markets.routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmarks.settings')
application = ProtocolTypeRouter({
    'http': app,
    'websocket': AuthMiddlewareStack(URLRouter(markets.routing.websocket_urlpatterns))
})
