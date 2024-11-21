from django.conf import settings
from asgiref.sync import async_to_sync
from markets.telegram import Telegram
import channels.layers
from redis import Redis


redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def send_message_to_ts(from_name, cids, message):
    bot_id = settings.TELEBOT_ID
    if bot_id:
        si = Telegram(bot_id).send_message(set(cids), f'{from_name}\n{message}')
        msg_ids = set()
        for cid in si:
            if si[cid] and si[cid]['ok']:
                msg_ids.add(si[cid]['result']['message_id'])
        for mid in msg_ids:
            key = f'questions:{mid}:from'
            redis.set(name=key, value=from_name, ex=3600)


def collect_messages_from_ts():
    bot_id = settings.TELEBOT_ID
    if bot_id:
        updates = Telegram(bot_id).get_updates()
        if updates and updates['ok']:
            for upd in updates['result']:
                if 'message' in upd and (message := upd['message']) is not None and 'reply_to_message' in message:
                    r_mid = message['reply_to_message']['message_id']
                    key = f'questions:{r_mid}:from'
                    if (from_name := redis.get(key)) is not None:
                        redis.delete(key)
                        channel_layer = channels.layers.get_channel_layer()
                        async_to_sync(channel_layer.group_send)(from_name.decode(), {'type': 'message_from_ts', 'message': message['text']})
