from celery import shared_task
from markets.api.business import restore_db_consistency


@shared_task
def do_rdc():
    restore_db_consistency()
