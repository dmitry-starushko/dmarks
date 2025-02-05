import httpx
from django.conf import settings
from markets.decorators import on_exception_returns
from markets.enums import FUS
from markets.models import DmUser


@on_exception_returns(dict())
def get_reg_card(user: DmUser):
    if not user.confirmed:
        raise RuntimeError(FUS.UNV)
    with httpx.Client() as client:
        res = client.get(settings.URLS_1C_API['reg-card'].format(user=user.aux_data.itn),
                         headers={'Authorization': settings.AUTH_1C_API} if settings.AUTH_1C_API else {})
        if res.is_error:
            raise RuntimeError(FUS.SRE)
        result = res.json()
    match result:
        case {**card}:
            for key, value in card.items():
                match key, value:
                    case str(_), str(_): pass
                    case _: raise RuntimeError(FUS.USR)
            return card
        case _: raise RuntimeError(FUS.USR)


@on_exception_returns(dict())
def get_market_info(mid: str):
    with httpx.Client() as client:
        res = client.get(settings.URLS_1C_API['market-info'].format(market=mid),
                         headers={'Authorization': settings.AUTH_1C_API} if settings.AUTH_1C_API else {})
        if res.is_error:
            raise RuntimeError(FUS.SRE)
        result = res.json()
    match result:
        case {**info}:
            for key, value in info.items():
                match key, value:
                    case str(_), str(_): pass
                    case _: raise RuntimeError(FUS.USR)
            return info
        case _: raise RuntimeError(FUS.USR)
