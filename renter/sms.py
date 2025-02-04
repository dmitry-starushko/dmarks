from markets.decorators import on_exception_returns


@on_exception_returns('@')
def send_sms_code(phone: str) -> str:
    return 'e39641da-7c2f-4cd9-9524-9ff785e56116'


@on_exception_returns(False)
def check_sms_code(code: str, uuid: str) -> bool:
    print(code, uuid)
    return code == '12345'
