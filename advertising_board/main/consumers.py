import json

from channels.generic.websocket import WebsocketConsumer

from .models import Ad


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self._search_ad(message)

    def _search_ad(self, message):
        ads = Ad.objects.search_ads(message)
        self.send(text_data=json.dumps({'message': ads}))
