from enum import StrEnum


class Observation(StrEnum):
    OUTLET_RENTING_COST_MIN = 'outlet-renting-cost-min'
    OUTLET_RENTING_COST_MAX = 'outlet-renting-cost-max'
    OUTLET_AREA_MIN = 'outlet-area-min'
    OUTLET_AREA_MAX = 'outlet-area-max'


class OutletState(StrEnum):
    UNKNOWN = 'UNKNOWN'
    AVAILABLE_FOR_BOOKING = 'AVAILFB'
    UNAVAILABLE_FOR_BOOKING = 'UNAVLFB'
    TEMPORARILY_UNAVAILABLE_FOR_BOOKING = 'TUNAVFB'
    BOOKED = 'BOOKED'
    RENTED = 'RENTED'


class NotificationType(StrEnum):
    INFORMATION = 'info'
    WARNING = 'warn'
    ALERT = 'alrt'


class LocationType(StrEnum):
    CITY = 'г.'
    DISTRICT = 'г.р-н'


class FUS(StrEnum):  # Frequently Used Strings
    NS = 'Не указано'
    UNV = 'Пользователь не верифицирован'
    SRE = 'Запрос к серверу завершился ошибкой'
    USR = 'Неожиданный ответ сервера'


class LogRecordKind(StrEnum):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    FATAL = 'fatal'
