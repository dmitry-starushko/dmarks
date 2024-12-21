from django.core.validators import RegexValidator


class Validators:
    CSS = '^#[\\da-fA-F]{6}$'
    HEX = '^0x[\\da-fA-F]{1,6}$'
    ONM = '^\\d{9}[а-яё]{0,1}$'
    MID = '^\\d{3}$'
    POC = '^\\d{5,6}$'
    ITN = '^((?:\\d{10})|(?:\\d{12}))$'

    @staticmethod
    def _rxv(rx: str, msg: str):
        return RegexValidator(regex=rx, message=msg)

    @staticmethod
    def css_color(value):
        return Validators._rxv(Validators.CSS, "Ожидается значение в формате #ffffff")(value)

    @staticmethod
    def hex(value):
        return Validators._rxv(Validators.HEX, "Ожидается значение в формате 0xffffff")(value)

    @staticmethod
    def outlet_number(value):
        return Validators._rxv(Validators.ONM, "Ожидается значение в формате 999999999[a]")(value)

    @staticmethod
    def market_id(value):
        return Validators._rxv(Validators.MID, "Ожидается значение в формате 999")(value)

    @staticmethod
    def postal_code(value):
        return Validators._rxv(Validators.POC, "Ожидается значение в формате 999999")(value)

    @staticmethod
    def itn(value):
        return Validators._rxv(Validators.ITN, "Ожидается значение в формате 999")(value)
