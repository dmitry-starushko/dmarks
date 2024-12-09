from enum import StrEnum


class Observation(StrEnum):
    OUTLET_RENTING_COST_MIN = 'outlet-renting-cost-min'
    OUTLET_RENTING_COST_MAX = 'outlet-renting-cost-max'


class OutletState(StrEnum):
    UNKNOWN = 'UNKNOWN'
    AVAILABLE_FOR_BOOKING = 'AVAILFB'
    UNAVAILABLE_FOR_BOOKING = 'UNAVLFB'
    TEMPORARILY_UNAVAILABLE_FOR_BOOKING = 'TUNAVFB'
    BOOKED = 'BOOKED'
    RENTED = 'RENTED'
