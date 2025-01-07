from django.db import transaction
from markets.enums import OutletState
from markets.models import DmUser, TradePlace, TradePlaceType


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
                        olet.trade_place_type = TradePlaceType.objects.get_or_create(type_name=OutletState.RENTED)[0]
                        olet.save()
                    else:
                        raise ValueError(number)
        case _: raise ValueError(data)
    return True


def unrent_outlets(user: DmUser, data):
    match data:
        case [*numbers]:
            with transaction.atomic():
                for number in numbers:
                    if isinstance(number, str):
                        olet: TradePlace = user.rented_outlets.get(location_number=number)
                        olet.rented_by = None
                        olet.trade_place_type = TradePlaceType.objects.get_or_create(type_name=OutletState.AVAILABLE_FOR_BOOKING)[0]
                        olet.save()
                    else:
                        raise ValueError(number)
        case _: raise ValueError(data)
    return True


def get_outlets_in_renting(user: DmUser):
    return [i['location_number'] for i in user.rented_outlets.values('location_number')]
