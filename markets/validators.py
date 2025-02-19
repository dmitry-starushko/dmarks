from django.core.validators import RegexValidator


class Validators:
    CSS = r'^#[\da-fA-F]{6}$'
    HEX = r'^0x[\da-fA-F]{1,6}$'
    ONM = r'^\d{9}[а-яё]{0,1}$'
    MID = r'^\d{3}$'
    POC = r'^\d{5,6}$'
    ITN = r'^((?:\d{10})|(?:\d{12}))$'
    PNE = r'^\+\d{1,3}\(\d{3}\)\d{3}-\d{2}-\d{2}$'

    @staticmethod
    def _rxv(rx: str):
        return RegexValidator(regex=rx, message=f'Значение не соответствует регулярному выражению {rx}')

    @staticmethod
    def css_color(value):
        return Validators._rxv(Validators.CSS)(value)

    @staticmethod
    def hex(value):
        return Validators._rxv(Validators.HEX)(value)

    @staticmethod
    def outlet_number(value):
        return Validators._rxv(Validators.ONM)(value)

    @staticmethod
    def market_id(value):
        return Validators._rxv(Validators.MID)(value)

    @staticmethod
    def postal_code(value):
        return Validators._rxv(Validators.POC)(value)

    @staticmethod
    def itn(value):
        return Validators._rxv(Validators.ITN)(value)

    @staticmethod
    def phone(value):
        return Validators._rxv(Validators.PNE)(value)
