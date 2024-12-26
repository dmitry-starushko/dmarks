import httpx
from django.conf import settings
from django.db import transaction
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
    if user.aux_data.passport_image is None:
        raise ConfirmationError('Отсутствует скан паспорта')
    with httpx.Client() as client:
        try:
            res = client.post(settings.EXT_URL['confirmation'].format(user=user.aux_data.itn),
                              headers={'Content-Type': 'application/json'},
                              json={
                                  'first-name': user.first_name,
                                  'last_name': user.last_name,
                                  'phone': user.phone,
                                  'email': user.email,
                                  'itn': user.aux_data.itn,
                                  'usrle': user.aux_data.usr_le_extract.as_dictionary,
                                  'passport': user.aux_data.passport_image.as_dictionary,
                              })
            if res.is_error:
                raise ConfirmationError(f'В верификации отказано: {res.text or 'без пояснений'}')
            return True
        except httpx.TransportError as e:
            raise ConfirmationError(f'Ошибка сети: {e}') from e


def set_user_confirmed(user: DmUser):
    if not user.confirmed:
        if not hasattr(user, 'aux_data'):
            raise ConfirmationError('Валидация не может быть проведена без предоставления дополнительных данных')
        with transaction.atomic():
            user.aux_data.confirmed = True
            user.aux_data.save()
            if user.aux_data.usr_le_extract is not None:
                user.aux_data.usr_le_extract.delete()
            if user.aux_data.passport_image is not None:
                user.aux_data.passport_image.delete()
    return True
