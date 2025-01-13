from markets.enums import LogRecordKind
from markets.models import DmUser
from markets.tasks import st_log


def dlog(user: DmUser | None, text: str, kind: LogRecordKind):
    st_log.delay(user.id if user is not None else None, text, kind)


def dlog_info(user: DmUser | None, text: str):
    dlog(user, text, LogRecordKind.INFO)


def dlog_warn(user: DmUser | None, text: str):
    dlog(user, text, LogRecordKind.WARNING)


def dlog_error(user: DmUser | None, text: str):
    dlog(user, text, LogRecordKind.ERROR)


def dlog_fatal(user: DmUser | None, text: str):
    dlog(user, text, LogRecordKind.FATAL)