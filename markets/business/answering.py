import httpx
from django.conf import settings
from markets.business.logimpl import ilog
from markets.enums import LogRecordKind


def deliver_answer(itn: str | None, question_uuid: str, answer: bool):
    with httpx.Client(timeout=settings.TIMEOUT_1C_API) as client:
        try:
            res = client.post(settings.URLS_1C_API['answers'].format(user=itn or '0000000000'),
                              headers={'Content-Type': 'application/json'} | ({'Authorization': settings.AUTH_1C_API} if settings.AUTH_1C_API else {}),
                              json={
                                  'user': itn,
                                  'question_uuid': question_uuid,
                                  'answer': answer})
            if res.is_error:
                ilog(None, f'Ответ {answer} на вопрос {question_uuid} от пользователя {itn} не доставлен: ответ сервера {res.status_code}', LogRecordKind.ERROR)
        except httpx.TransportError as e:
            ilog(None, f'Ответ {answer} на вопрос {question_uuid} от пользователя {itn} не доставлен: исключение {e}', LogRecordKind.ERROR)
