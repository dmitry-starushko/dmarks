import httpx
from django.conf import settings
from django.db import transaction

from markets.decorators import on_exception_returns
from markets.enums import OutletState, FUS
from markets.models import DmUser, TradePlace


def rent_outlets(user: DmUser, data):
    if not user.confirmed:
        raise ValueError(f'Пользователь {user.aux_data.itn} не верифицирован')
    match data:
        case [*numbers]:
            with transaction.atomic():
                for number in numbers:
                    if isinstance(number, str):
                        olet: TradePlace = TradePlace.objects.get(location_number=number)
                        if olet.rented_by is not None:
                            raise ValueError(f'Торговое место {number} уже арендовано')
                        olet.rented_by = user
                        olet.trade_place_type = OutletState.RENTED
                        olet.save()
                    else:
                        raise ValueError(number)
        case _: raise ValueError(data)
    return True


@on_exception_returns(frozenset())
def get_outlets_in_renting(user: DmUser):
    return False
    # if not user.confirmed:
    #     raise RuntimeError(FUS.UNV)
    # with httpx.Client() as client:
    #     res = client.get(settings.EXT_URL['booking'].format(user=user.aux_data.itn))
    #     if res.is_error:
    #         raise RuntimeError(FUS.SRE)
    #     result = res.json()
    # match result:
    #     case [*items]: return frozenset(f'{i}' for i in items)
    #     case _: raise RuntimeError(FUS.USR)


@on_exception_returns(frozenset())
def unrent_outlets(user: DmUser, data):
    return False
    # if not user.confirmed:
    #     raise RuntimeError(FUS.UNV)
    # with httpx.Client() as client:
    #     res = client.delete(settings.EXT_URL['booking'].format(user=user.aux_data.itn))
    #     if res.is_error:
    #         raise RuntimeError(FUS.SRE)
    #     result = res.json()
    # match result:
    #     case [*items]: return frozenset(f'{i}' for i in items)
    #     case _: raise RuntimeError(FUS.USR)
