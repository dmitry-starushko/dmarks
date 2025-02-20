from django.conf import settings
from markets.enums import LogRecordKind
from markets.models import DmUser, LogRecord


def ilog(upk: int | None, text: str, kind=LogRecordKind.INFO):
    if kind in settings.LOG_KINDS:
        try:
            user = DmUser.objects.get(pk=upk)
        except DmUser.DoesNotExist:
            user = None
        LogRecord.objects.create(user=user, kind=kind, text=text)
