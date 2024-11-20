import os
from celery import shared_task
from django.conf import settings
from markets.business.actions import restore_db_consistency
from markets.telegram import Telegram


@shared_task
def st_restore_db_consistency():
    restore_db_consistency()


@shared_task
def st_send_telegram_message(cids, message):
    bot_id = settings.TELEBOT_ID
    if bot_id:
        Telegram(bot_id).send_message(set(cids), message)
