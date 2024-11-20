from django.conf import settings
from markets.telegram import Telegram


def send_message_to_ts(cids, message):
    bot_id = settings.TELEBOT_ID
    if bot_id:
        Telegram(bot_id).send_message(set(cids), message)
