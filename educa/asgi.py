import os
from django.core.asgi import get_asgi_application

#frist because we need to set up the enviroment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educa.settings')

#this has to stay on top because, django need to run the django asgi app first(basically make the asgi functionality working)
django_asgi_app = get_asgi_application()

#then import stuff, so it work afte the asgi run properly
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(websocket_urlpatterns)
        )
    )
    
})