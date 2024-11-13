from celery import shared_task
from markets.business.actions import restore_db_consistency


@shared_task
def st_restore_db_consistency():
    restore_db_consistency()
