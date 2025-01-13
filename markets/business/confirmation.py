import httpx
from django.conf import settings
from django.db import transaction
from markets.decorators import on_exception_returns
from markets.enums import FUS
from markets.models import DmUser


class ConfirmationError(Exception):
    def __init__(self, message):
        super().__init__(message)


def init_confirmation(user: DmUser):  # TODO text from params
    if user.confirmed:
        raise ConfirmationError('Верификация уже пройдена')
    if not hasattr(user, 'aux_data'):
        raise ConfirmationError('Для начала процесса валидации необходимо указать дополнительные персональные данные')
    if user.aux_data.usr_le_extract is None:
        raise ConfirmationError('Отсутствует выписка из ЕГРЮЛ')
    # if user.aux_data.passport_image is None:
    #     raise ConfirmationError('Отсутствует скан паспорта')
    with httpx.Client() as client:
        try:
            res = client.post(settings.EXT_URL['confirmation'].format(user=user.aux_data.itn),
                              headers={'Content-Type': 'application/json'},
                              json={
                                  'first-name': user.first_name,
                                  'last-name': user.last_name,
                                  'phone': user.phone,
                                  'email': user.email,
                                  'itn': user.aux_data.itn,
                                  'usrle': user.aux_data.usr_le_extract.as_dictionary,
                                  # 'passport': user.aux_data.passport_image.as_dictionary,
                              })
            if res.is_error:
                raise ConfirmationError(f'В верификации отказано: {res.text or 'без пояснений'}')
            return True
        except httpx.TransportError as e:
            raise ConfirmationError(f'Ошибка сети: {e}') from e


def set_user_confirmed(user: DmUser, data):
    match data:
        case bool(value):
            if value:
                if not hasattr(user, 'aux_data'):
                    raise ConfirmationError('Дополнительные данные отсутствуют')
                if not user.confirmed:
                    with transaction.atomic():
                        user.aux_data.confirmed = True
                        user.aux_data.save()
                        if user.aux_data.usr_le_extract is not None:
                            user.aux_data.usr_le_extract.delete()
                        if user.aux_data.passport_image is not None:
                            user.aux_data.passport_image.delete()
            else:
                if hasattr(user, 'aux_data'):
                    user.aux_data.delete()
            return True
        case _: raise ValueError(data)


@on_exception_returns(dict())
def get_reg_card(user: DmUser):
    if not user.confirmed:
        raise RuntimeError(FUS.UNV)
    with httpx.Client() as client:
        res = client.get(settings.EXT_URL['reg-card'].format(user=user.aux_data.itn))
        if res.is_error:
            raise RuntimeError(FUS.SRE)
        result = res.json()
    match result:
        case {**card}:
            for key, value in card.items():
                match key, value:
                    case str(_), str(_): pass
                    case _: raise RuntimeError(FUS.USR)
            return card
        case _: raise RuntimeError(FUS.USR)

