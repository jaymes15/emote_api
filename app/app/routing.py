from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from chats.consumers import ChatConsumer
from chats.middlewares import TokenAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter([
           
            re_path(r"ws/chat/(?P<username>[a-zA-Z0-9-_=]+)/$", ChatConsumer.as_asgi()),
        ])
    )
})