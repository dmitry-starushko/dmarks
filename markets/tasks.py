import os
from celery import shared_task
from markets.business.actions import restore_db_consistency
from markets.business.tech_support import send_message_to_ts


@shared_task
def st_restore_db_consistency():
    restore_db_consistency()


@shared_task
def st_send_message_to_ts(from_name, cids, message):
    send_message_to_ts(from_name, cids, message)
