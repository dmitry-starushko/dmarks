import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from markets.models import Parameter
from markets.tasks import st_send_message_to_ts


class ChatConsumer(WebsocketConsumer):
    @property
    def ts_cids(self):
        try:
            return {int(cid) for cid in Parameter.value_of('ts_chat_ids').split(':')}
        except ValueError:
            return set()

    @property
    def group_name(self):
        return f'user_{hash(self.channel_name)}'

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        print(f'disconnected with code {close_code}')
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # self.send(text_data=json.dumps({'message': f'Вы написали мне: "{message}". Лучшие специалисты планеты уже обдумывают Вашу проблему! Продолжайте наблюдение.'}))
        st_send_message_to_ts.delay(self.group_name, list(self.ts_cids), message)

    def message_from_ts(self, event):
        self.send(text_data=json.dumps(event))
