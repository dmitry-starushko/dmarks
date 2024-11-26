import os
from celery import shared_task
from dmarks import celery
from markets.business.actions import restore_db_consistency, observe_all
from markets.business.tech_support import send_message_to_ts, collect_messages_from_ts


@celery.app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, pt_collect_messages_from_ts.s(), name='collect messages')
    sender.add_periodic_task(3600.0, pt_observe_all.s(), name='observe all observables')


@celery.app.task
def pt_collect_messages_from_ts():
    collect_messages_from_ts()


@celery.app.task
def pt_observe_all():
    observe_all()


@shared_task
def st_restore_db_consistency():
    restore_db_consistency()


@shared_task
def st_send_message_to_ts(from_name, cids, message):
    send_message_to_ts(from_name, cids, message)
