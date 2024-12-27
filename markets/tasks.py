from celery import shared_task
from dmarks import celery
from markets.business.actions import restore_db_consistency, observe_all, delete_obsolete_notifications, logrotate
from markets.business.tech_support import send_message_to_ts, collect_messages_from_ts


@celery.app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(11.0, pt_collect_messages_from_ts.s(), name='collect messages')
    sender.add_periodic_task(3600.0, pt_observe_all.s(), name='observe all observables')
    sender.add_periodic_task(13 * 3600.0, pt_delete_obsolete_notifications.s(), name='delete obsolete notifications')
    sender.add_periodic_task(17 * 3600.0, pt_delete_obsolete_notifications.s(), name='logrotate')


@celery.app.task
def pt_collect_messages_from_ts():
    collect_messages_from_ts()


@celery.app.task
def pt_observe_all():
    observe_all()


@celery.app.task
def pt_logrotate():
    logrotate()


@celery.app.task
def pt_delete_obsolete_notifications():
    delete_obsolete_notifications()


@shared_task
def st_restore_db_consistency():
    restore_db_consistency()


@shared_task
def st_send_message_to_ts(from_name, cids, message):
    send_message_to_ts(from_name, cids, message)
