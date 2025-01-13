import httpx
from django.conf import settings


def send_question_answer(itn: str, question_uuid: str, answer: bool):
    with httpx.Client() as client:
        try:
            res = client.post(settings.EXT_URL['confirmation'],
                              headers={'Content-Type': 'application/json'},
                              json={
                                  'user': itn,
                                  'question_uuid': question_uuid,
                                  'answer': answer
                              })
            if res.is_error:
                pass  # TODO log undelivered answer
        except httpx.TransportError as e:
            pass  # TODO log undelivered answer
