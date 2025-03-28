import httpx
import re
from django.conf import settings
from markets.decorators import on_exception_returns


@on_exception_returns('@')
def send_sms_code(phone: str) -> str:
    phone = re.sub(r'\D', '', phone)
    with httpx.Client() as client:
        res = client.post(settings.URLS_SMS_API['send'],
                          headers={'Content-Type': 'application/json', 'Authorization': settings.AUTH_SMS_API},
                          json={"gatewayId": "1Gx5IJ", "channelType": "SMS", "destination": phone})
        if res.is_error:
            raise ValueError(res)
        return res.json()['uuid']


@on_exception_returns(False)
def check_sms_code(code: str, uuid: str) -> bool:
    with httpx.Client() as client:
        res = client.post(settings.URLS_SMS_API['check'],
                          headers={'Content-Type': 'application/json', 'Authorization': settings.AUTH_SMS_API},
                          json={"uuid": uuid, "code": code})
        return False if res.is_error else (res.json()['status'] == 'CONFIRMED')
