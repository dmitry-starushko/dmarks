import httpx
from django.conf import settings
from markets.business.logimpl import ilog
from markets.decorators import on_exception_returns
from markets.enums import LogRecordKind
from markets.models import DmUser


@on_exception_returns(None)
def moderate_promo_data(itn: str):
    user: DmUser = DmUser.objects.get(aux_data__itn=itn)
    with httpx.Client() as client:
        try:
            res = client.post(settings.URLS_1C_API['moderation'].format(user=itn),
                              headers={'Content-Type': 'application/json'},
                              json={'text': user.promo_text, 'image': user.promo_image.url if user.promo_image else ''})
            if res.is_error:
                ilog(user.id, f'Запрос на модерацию промо-данных пользователя {itn} не доставлен: ответ сервера {res.status_code}', LogRecordKind.ERROR)
        except httpx.TransportError as e:
            ilog(user.id, f'Запрос на модерацию промо-данных пользователя {itn} не доставлен: исключение {e}', LogRecordKind.ERROR)


def set_promo_data_moderated(user: DmUser, data):
    match data:
        case bool(value):
            status = 'Одобрено' if value else 'Не одобрено'
            ilog(user.id, f'Запрошено изменение статуса промо-данных пользователя {user.phone} на «{status}»', LogRecordKind.INFO)
            if hasattr(user, 'aux_data'):
                user.aux_data.promo_enabled = value
                user.aux_data.save()
                ilog(user.id, f'Статуса промо-данных пользователя {user.phone} изменен на «{status}»', LogRecordKind.INFO)
            else:
                ilog(user.id, f'Статус промо-данных пользователя {user.phone} не может быть изменен: нет данных', LogRecordKind.WARNING)
            return True
        case _: raise ValueError(data)
