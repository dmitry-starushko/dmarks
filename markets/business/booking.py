import httpx
from django.conf import settings
from markets.business.logging import dlog_info, dlog_error, dlog_warn
from markets.decorators import on_exception_returns
from markets.enums import OutletState, FUS
from markets.models import DmUser, TradePlace


class BookingError(Exception):
    def __init__(self, message):
        super().__init__(message)


def book_outlet(user: DmUser, outlet: TradePlace):
    if not user.confirmed:
        raise BookingError('Для бронирования торгового места необходимо пройти процедуру верификации в личном кабинете')
    if outlet.trade_place_type.type_name != OutletState.AVAILABLE_FOR_BOOKING:
        raise BookingError(f'Статус торгового места {outlet.location_number}: {outlet.trade_place_type}')
    dlog_info(user, f'Пользователь {user.phone} запросил бронирование ТМ {outlet.location_number}')
    with httpx.Client() as client:
        try:
            res = client.post(settings.EXT_URL['booking'].format(user=user.aux_data.itn),
                              headers={'Content-Type': 'application/json'},
                              json=[f'{outlet.location_number}'])
            if res.is_error:
                reason = f'{res.text or 'без пояснений'}'
                dlog_warn(user, f'Пользователю {user.phone} отказано в бронировании {outlet.location_number}: {reason}')
                raise BookingError(f'В бронировании отказано: {reason}')
            return True
        except httpx.TransportError as e:
            dlog_error(user, f'Запрос пользователя {user.phone} на бронирование {outlet.location_number} не удалось отправить: {e}')
            raise BookingError(f'Ошибка сети: {e}') from e


@on_exception_returns(frozenset())
def get_outlets_in_booking(user: DmUser):
    if not user.confirmed:
        raise RuntimeError(FUS.UNV)
    with httpx.Client() as client:
        res = client.get(settings.EXT_URL['booking'].format(user=user.aux_data.itn))
        if res.is_error:
            raise RuntimeError(FUS.SRE)
        result = res.json()
    match result:
        case [*items]: return frozenset(f'{i}' for i in items)
        case _: raise RuntimeError(FUS.USR)


@on_exception_returns(frozenset())
def unbook_all(user: DmUser):
    if not user.confirmed:
        raise RuntimeError(FUS.UNV)
    with httpx.Client() as client:
        res = client.delete(settings.EXT_URL['booking'].format(user=user.aux_data.itn))
        if res.is_error:
            raise RuntimeError(FUS.SRE)
        result = res.json()
    match result:
        case [*items]: return frozenset(f'{i}' for i in items)
        case _: raise RuntimeError(FUS.USR)
