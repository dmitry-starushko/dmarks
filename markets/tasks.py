import os
from celery import shared_task
from dmarks import celery
from markets.business.actions import restore_db_consistency
from markets.business.tech_support import send_message_to_ts, collect_messages_from_ts


@celery.app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, pt_collect_messages_from_ts.s(), name='collect messages')


@celery.app.task
def pt_collect_messages_from_ts():
    collect_messages_from_ts()


@shared_task
def st_restore_db_consistency():
    restore_db_consistency()


@shared_task
def st_send_message_to_ts(from_name, cids, message):
    send_message_to_ts(from_name, cids, message)
