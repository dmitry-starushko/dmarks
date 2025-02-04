from django.db import transaction
from markets.business.logging import dlog_info
from markets.enums import OutletState
from markets.models import DmUser, TradePlace, TradePlaceType


def rent_outlets(user: DmUser, data):
    if not user.confirmed:
        raise ValueError(f'Пользователь {user.itn} не верифицирован')
    match data:
        case [*numbers]:
            dlog_info(user, f'Получен запрос на включение торговых мест {', '.join(numbers)} в арендный список пользователя {user.phone}')
            with transaction.atomic():
                for number in numbers:
                    if isinstance(number, str):
                        outlet: TradePlace = TradePlace.objects.get(location_number=number)
                        if outlet.rented_by is not None:
                            if outlet.rented_by.id == user.id:
                                continue
                            else:
                                raise ValueError(f'Торговое место {number} арендовано другим арендатором')
                        outlet.rented_by = user
                        outlet.trade_place_type = TradePlaceType.objects.get_or_create(type_name=OutletState.RENTED)[0]
                        outlet.save()
                    else:
                        raise ValueError(number)
        case _: raise ValueError(data)
    dlog_info(user, f'Запрос на включение торговых мест {', '.join(numbers)} в арендный список пользователя {user.phone} выполнен')
    return True


def unrent_outlets(user: DmUser, data):
    match data:
        case [*numbers]:
            dlog_info(user, f'Получен запрос на исключение торговых мест {', '.join(numbers)} из арендного списка пользователя {user.phone}')
            with transaction.atomic():
                for number in numbers:
                    if isinstance(number, str):
                        outlet: TradePlace = user.rented_outlets.get(location_number=number)
                        outlet.rented_by = None
                        outlet.trade_place_type = TradePlaceType.objects.get_or_create(type_name=OutletState.UNKNOWN)[0]
                        outlet.save()
                    else:
                        raise ValueError(number)
        case _: raise ValueError(data)
    dlog_info(user, f'Запрос на исключение торговых мест {', '.join(numbers)} из арендного списка пользователя {user.phone} выполнен')
    return True


def get_outlets_in_renting(user: DmUser):
    return [i['location_number'] for i in user.rented_outlets.values('location_number')]
