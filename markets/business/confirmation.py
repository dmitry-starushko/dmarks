import httpx
from django.conf import settings
from django.db import transaction
from markets.business.logging import dlog_info, dlog_error, dlog_warn
from markets.models import DmUser


class ConfirmationError(Exception):
    def __init__(self, message):
        super().__init__(message)


def init_confirmation(user: DmUser):
    if user.confirmed:
        raise ConfirmationError('Верификация уже пройдена')
    if not hasattr(user, 'aux_data'):
        raise ConfirmationError('Для начала процесса валидации необходимо указать дополнительные персональные данные')
    if user.aux_data.usr_le_extract is None:
        raise ConfirmationError('Отсутствует выписка из ЕГРЮЛ/ЕГРИП')
    # if user.aux_data.passport_image is None:
    #     raise ConfirmationError('Отсутствует скан паспорта')
    dlog_info(user, f'Пользователь {user.phone} инициировал процедуру верификации (ИНН: {user.itn})')
    with httpx.Client(timeout=settings.TIMEOUT_1C_API) as client:
        try:
            res = client.post(settings.URLS_1C_API['confirmation'].format(user=user.itn),
                              headers={'Content-Type': 'application/json'} | ({'Authorization': settings.AUTH_1C_API} if settings.AUTH_1C_API else {}),
                              json={
                                  'first-name': user.first_name,
                                  'last-name': user.last_name,
                                  'phone': user.phone,
                                  'email': user.email,
                                  'itn': user.itn,
                                  'usrle': user.aux_data.usr_le_extract.as_dictionary,
                                  # 'passport': user.aux_data.passport_image.as_dictionary,
                              })
            if res.is_error:
                reason = f'{res.text or 'без пояснений'}'
                dlog_warn(user, f'Пользователю {user.phone} отказано в процедуре верификации: {reason}')
                raise ConfirmationError(f'В верификации отказано: {reason}')
            dlog_info(user, f'Запрос пользователя {user.phone} на инициацию процедуры верификации отправлен серверу')
            return True
        except httpx.TransportError as e:
            dlog_error(user, f'Запрос пользователя {user.phone} на верификацию не удалось отправить: {e}')
            raise ConfirmationError(f'Ошибка сети: {e}') from e


def set_user_confirmed(user: DmUser, data):
    match data:
        case bool(value):
            dlog_info(user, f'Запрошено изменение статуса верификации пользователя {user.phone} на «{'Верифицирован' if value else 'Не верифицирован'}»')
            if value:
                if not hasattr(user, 'aux_data'):
                    dlog_warn(user, f'Статус пользователя {user.phone} не может быть изменен на «Верифицирован»: нет данных')
                    raise ConfirmationError('Дополнительные данные отсутствуют')
                if not user.confirmed:
                    with transaction.atomic():
                        user.aux_data.confirmed = True
                        user.aux_data.save()
                        if user.aux_data.usr_le_extract is not None:
                            user.aux_data.usr_le_extract.delete()
                        if user.aux_data.passport_image is not None:
                            user.aux_data.passport_image.delete()
                    dlog_info(user, f'Статус пользователя {user.phone} изменен на «Верифицирован»')
                else:
                    dlog_info(user, f'Статус пользователя {user.phone} «Верифицирован»; статус не изменился')
            else:
                if hasattr(user, 'aux_data'):
                    user.aux_data.delete()
                    dlog_info(user, f'Статус пользователя {user.phone} изменен на «Не верифицирован»')
                else:
                    dlog_info(user, f'Статус пользователя {user.phone} «Не верифицирован»; статус не изменился')
            return True
        case _: raise ValueError(data)
