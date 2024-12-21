from django.core.validators import RegexValidator


class Validators:
    @staticmethod
    def _rxv(rx: str, msg: str):
        return RegexValidator(regex=rx, message=msg)

    @staticmethod
    def css_color(value):
        return Validators._rxv('^#[\\da-fA-F]{6}$', "Ожидается значение в формате #ffffff")(value)

    @staticmethod
    def hex(value):
        return Validators._rxv('^0x[\\da-fA-F]{1,6}$', "Ожидается значение в формате 0xffffff")(value)

    @staticmethod
    def outlet_number(value):
        return Validators._rxv('^\\d{9}[а-яё]{0,1}$', "Ожидается значение в формате 999999999[a]")(value)

    @staticmethod
    def market_id(value):
        return Validators._rxv('^\\d{3}$', "Ожидается значение в формате 999")(value)

    @staticmethod
    def postal_code(value):
        return Validators._rxv('^\\d{5,6}$', "Ожидается значение в формате 999999")(value)

    @staticmethod
    def itn(value):
        return Validators._rxv('^((?:\\d{10})|(?:\\d{12}))$', "Ожидается значение в формате 999")(value)
