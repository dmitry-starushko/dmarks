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
    dlog_info(user, f'Пользователь {user.phone} инициировал заявку на бронирование ТМ {outlet.location_number}')
    with httpx.Client(timeout=settings.TIMEOUT_1C_API) as client:
        try:
            res = client.post(settings.URLS_1C_API['booking'].format(user=user.itn),
                              headers={'Content-Type': 'application/json'} | ({'Authorization': settings.AUTH_1C_API} if settings.AUTH_1C_API else {}),
                              json=[f'{outlet.location_number}'])
            if res.is_error:
                reason = f'{res.text or 'без пояснений'}'
                dlog_warn(user, f'Пользователю {user.phone} отказано в бронировании {outlet.location_number}: {reason}')
                raise BookingError(f'В бронировании отказано: {reason}')
            dlog_info(user, f'Запрос пользователя {user.phone} на бронирование ТМ {outlet.location_number} отправлен')
            return True
        except httpx.TransportError as e:
            dlog_error(user, f'Запрос пользователя {user.phone} на бронирование {outlet.location_number} не удалось отправить: {e}')
            raise BookingError(f'Ошибка сети: {e}') from e


@on_exception_returns(frozenset())
def get_outlets_in_booking(user: DmUser):
    if not user.confirmed:
        raise RuntimeError(FUS.UNV)
    with httpx.Client(timeout=settings.TIMEOUT_1C_API) as client:
        res = client.get(settings.URLS_1C_API['booking'].format(user=user.itn),
                         headers={'Authorization': settings.AUTH_1C_API} if settings.AUTH_1C_API else {})
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
    dlog_info(user, f'Пользователь {user.phone} запросил аннулирование всех запросов на бронирование ТМ')
    with httpx.Client(timeout=settings.TIMEOUT_1C_API) as client:
        try:
            res = client.delete(settings.URLS_1C_API['booking'].format(user=user.itn),
                                headers={'Authorization': settings.AUTH_1C_API} if settings.AUTH_1C_API else {})
            if res.is_error:
                reason = f'{res.text or 'без пояснений'}'
                dlog_warn(user, f'Запрос пользователя {user.phone} на аннулирование всех запросов на бронирование ТМ отклонен сервером: {reason}')
                raise RuntimeError(FUS.SRE)
            result = res.json()
            match result:
                case [*items]:
                    dlog_info(user, f'Запрос пользователя {user.phone} на аннулирование всех запросов на бронирование ТМ завершен успешно')
                    return frozenset(f'{i}' for i in items)
                case _: raise RuntimeError(FUS.USR)
        except httpx.TransportError as e:
            dlog_error(user, f'Запрос пользователя {user.phone} на аннулирование всех запросов на бронирование ТМ не удалось отправить: {e}')
            raise RuntimeError(f'Ошибка сети: {e}') from e
