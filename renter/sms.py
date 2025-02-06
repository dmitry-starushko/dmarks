import httpx
from django.conf import settings
from markets.decorators import on_exception_returns


@on_exception_returns('@')
def send_sms_code(phone: str) -> str:
    with httpx.Client() as client:
        res = client.post(settings.URLS_SMS_API['send'],
              headers={'Content-Type': 'application/json'} | ({'Authorization': settings.AUTH_SMS_API} if settings.AUTH_SMS_API else {}),
              json={"gatewayId": "1Gx5IJ", "channelType": "SMS", "destination": phone})
        datares = res.json()
        if res.is_error:
            return "Сервис недоступный"
        return datares['uuid']



@on_exception_returns(False)
def check_sms_code(code: str, uuid: str) -> bool:
    print(code, uuid)
    with httpx.Client() as client:
        res = client.post(settings.URLS_SMS_API['confirmation'],
              headers={'Content-Type': 'application/json'} | ({'Authorization': settings.AUTH_SMS_API} if settings.AUTH_SMS_API else {}),
              json={"uuid": uuid, "code": code})
        datares = res.json()
        if res.is_error:
            return False
    return datares['status'] == 'CONFIRMED'
