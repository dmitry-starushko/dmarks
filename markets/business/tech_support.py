import channels.layers
from django.conf import settings
from asgiref.sync import async_to_sync
from markets.telegram import Telegram
from redis import Redis


redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def send_message_to_ts(from_name, cids, message):
    bot_id = settings.TELEBOT_ID
    if bot_id:
        si = Telegram(bot_id).send_message(set(cids), f'{from_name}:\n{message}')
        msg_ids = set()
        redis.keys();
        for cid in si:
            if si[cid] and si[cid]['ok']:
                msg_ids.add(si[cid]['result']['message_id'])
        for mid in msg_ids:
            key = f'questions:{mid}:from'
            redis.set(name=key, value=from_name, ex=1800)


def collect_messages_from_ts():
    bot_id = settings.TELEBOT_ID
    if bot_id and redis.keys("questions:*:from"):
        updates = (tbot := Telegram(bot_id)).get_updates()
        if updates is not None and updates['ok']:
            for upd in updates['result']:
                if 'message' in upd and (message := upd['message']) is not None:
                    if 'reply_to_message' in message:
                        r_mid = message['reply_to_message']['message_id']
                        key = f'questions:{r_mid}:from'
                        if (from_name := redis.get(key)) is not None:
                            redis.delete(key)
                            channel_layer = channels.layers.get_channel_layer()
                            async_to_sync(channel_layer.group_send)(from_name.decode(), {'type': 'message_from_ts', 'message': message['text']})
                    else:
                        w_cid = message['from']['id']
                        w_mid = message['message_id']
                        w_key = f'warnings:{w_cid}:{w_mid}'
                        if not redis.exists(w_key):
                            redis.set(name=w_key, value=1, ex=3600*25)
                            tbot.send_message({message['from']['id']}, f'*Безадресные* сообщения *не допускаются*! Отвечайте на сообщения клиента!', True)
