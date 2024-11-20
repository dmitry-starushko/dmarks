import json
from channels.generic.websocket import WebsocketConsumer
from markets.tasks import st_send_telegram_message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print(f'disconnected with code {close_code}')
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({'message': f'Вы написали мне: "{message}". Лучшие специалисты планеты обдумывают Вашу проблему! Продолжайте наблюдение.'}))
        st_send_telegram_message.delay([1026778837], message)
