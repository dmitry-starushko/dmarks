import json
from channels.generic.websocket import WebsocketConsumer

from markets.models import Parameter
from markets.tasks import st_send_telegram_message


class ChatConsumer(WebsocketConsumer):
    @property
    def ts_cids(self):
        try:
            return {int(cid) for cid in Parameter.value_of('ts_chat_ids').split(':')}
        except ValueError:
            return set()

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print(f'disconnected with code {close_code}')
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({'message': f'Вы написали мне: "{message}". Лучшие специалисты планеты обдумывают Вашу проблему! Продолжайте наблюдение.'}))
        st_send_telegram_message.delay(list(self.ts_cids), message)
