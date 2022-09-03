from django.urls import path

from . import consumers


ws_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi())
]
