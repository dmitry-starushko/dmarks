import httpx
from django.conf import settings
from markets.decorators import on_exception_returns
from markets.enums import OutletState
from markets.models import DmUser, TradePlace


class BookingError(Exception):
    def __init__(self, message):
        super().__init__(message)


def book_outlet(user: DmUser, outlet: TradePlace):
    if user.aux_data is None or not user.aux_data.confirmed:
        raise BookingError('Пользователь не прошел процедуру валидации')
    if outlet.trade_place_type.type_name != OutletState.AVAILABLE_FOR_BOOKING:
        raise BookingError(f'Статус торгового места {outlet.location_number}: {outlet.trade_place_type}')
    with httpx.Client() as client:
        try:
            res = client.post(settings.EXT_URL['booking'].format(user=user.aux_data.itn),
                              headers={'Content-Type': 'application/json'},
                              json=[f'{outlet.location_number}'])
            if res.is_error:
                raise BookingError(f'В бронировании отказано: {res.text or 'без пояснений'}')
            return True
        except httpx.TransportError as e:
            raise BookingError(f'Ошибка сети: {e}') from e


@on_exception_returns(frozenset())
def get_booked_outlets(user: DmUser):
    if user.aux_data is None or not user.aux_data.confirmed:
        raise RuntimeError()
    with httpx.Client() as client:
        res = client.get(settings.EXT_URL['booking'].format(user=user.aux_data.itn))
        if res.is_error:
            raise RuntimeError()
        result = res.json()
    match result:
        case [*items]: return frozenset(f'{i}' for i in items)
        case _: raise RuntimeError()


def unbook_all(user_id):
    pass
