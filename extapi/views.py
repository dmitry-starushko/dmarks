from django.conf import settings
from django.http import HttpResponseBadRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import fields
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from extapi.openapi import oapi_market_serializer, oapi_result, oapi_outlet_serializer, oapi_notification_serializer
from markets.business.confirmation import set_user_confirmed
from markets.business.crud_entities import create_market, update_market, get_market, delete_market, create_market_outlets, get_market_outlets, update_market_outlets, delete_market_outlets, \
    create_market_schemes, get_market_schemes, update_market_schemes, delete_market_schemes, create_market_images, get_market_images, update_market_images, delete_market_images, create_market_phones, \
    get_market_phones, update_market_phones, delete_market_phones, create_market_emails, get_market_emails, update_market_emails, delete_market_emails, create_notifications, get_notifications, \
    delete_notifications
from markets.business.moderation import set_promo_data_moderated
from markets.business.renting import rent_outlets, get_outlets_in_renting, unrent_outlets
from markets.decorators import on_exception_returns_response
from markets.models import DmUser
from markets.business.actions import restore_db_consistency
from markets.tasks import st_restore_db_consistency


class MarketCRUDView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @extend_schema(
        description='Создает рынок с кодом mid.',
        request={'application/json': oapi_market_serializer(True, '_create_market')},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_create_market'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, mid):
        result = create_market(mid, request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Возвращает информацию о рынке с кодом mid.',
        responses={
            (200, 'application/json'): oapi_result(oapi_market_serializer(True, '_get_market'), '_get_market'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, _, mid):
        result = get_market(mid)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Изменяет данные рынка с кодом mid.',
        request={'application/json': oapi_market_serializer(False, '_update_market')},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_update_market'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, mid):
        result = update_market(mid, request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Удаляет рынок с кодом mid и все относящиеся к нему торговые места.',
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_delete_market'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, _, mid):
        result = delete_market(mid)
        return Response({
            'result': result
        })


class MarketOutletsCRUDView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @extend_schema(
        description='Создает торговые места для рынка с кодом mid.',
        request={'application/json': oapi_outlet_serializer(True, '_create_outlets')},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_create_outlets'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, mid):
        result = create_market_outlets(mid, request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Возвращает информацию о торговых местах рынка с кодом mid.',
        responses={
            (200, 'application/json'): oapi_result(oapi_outlet_serializer(True, '_get_outlets'), '_get_outlets'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, mid):
        result = get_market_outlets(mid)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Изменяет данные торговых мест рынка с кодом mid.',
        request={'application/json': oapi_outlet_serializer(False, '_update_outlets')},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_update_outlets'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, mid):
        result = update_market_outlets(mid, request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Удаляет торговые места рынка с кодом mid. Номера удаляемых торговых мест передаются в теле запроса как список строк. OpenAPI не позволяет вызвать этот метод.',
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_delete_outlets'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, mid):
        result = delete_market_outlets(mid, request.data)
        return Response({
            'result': result
        })


@extend_schema(exclude=True)
class MarketSchemesCRUDView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, mid):
        result = create_market_schemes(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, mid):
        result = get_market_schemes(mid)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, mid):
        result = update_market_schemes(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, mid):
        result = delete_market_schemes(mid, request.data)
        return Response({
            'result': result
        })


@extend_schema(exclude=True)
class MarketImagesCRUDView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, mid):
        result = create_market_images(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, mid):
        result = get_market_images(mid)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, mid):
        result = update_market_images(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, mid):
        result = delete_market_images(mid, request.data)
        return Response({
            'result': result
        })


@extend_schema(exclude=True)
class MarketPhonesCRUDView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, mid):
        result = create_market_phones(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, mid):
        result = get_market_phones(mid)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, mid):
        result = update_market_phones(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, mid):
        result = delete_market_phones(mid, request.data)
        return Response({
            'result': result
        })


@extend_schema(exclude=True)
class MarketEmailsCRUDView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, mid):
        result = create_market_emails(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, mid):
        result = get_market_emails(mid)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, mid):
        result = update_market_emails(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, mid):
        result = delete_market_emails(mid, request.data)
        return Response({
            'result': result
        })


class UserConfirmedView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @extend_schema(
        description='Устанавливает значение флага верификации для пользователя с ИНН = itn.\n'
                    'Сброс флага приводит к дальнейшей невалидности ИНН пользователя и необходимости повторной подачи заявки на верификацию.',
        request={'application/json': bool},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_set_confirmed'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, itn):
        result = set_user_confirmed(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Устанавливает значение флага верификации для пользователя с ИНН = itn.\n'
                    'Сброс флага приводит к дальнейшей невалидности ИНН пользователя и необходимости повторной подачи заявки на верификацию.',
        request={'application/json': bool},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_update_confirmed'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, itn):
        result = set_user_confirmed(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Возвращает значение флага верификации для пользователя с ИНН = itn',
        request={'application/json': bool},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат, значение флага'), '_get_confirmed'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, _, itn):
        result = DmUser.objects.get(aux_data__itn=itn).confirmed
        return Response({
            'result': result
        })


class UserModeratedView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @extend_schema(
        description='Устанавливает значение флага модерации промо-данных для пользователя с ИНН = itn.',
        request={'application/json': bool},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_set_moderated'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, itn):
        result = set_promo_data_moderated(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Устанавливает значение флага модерации промо-данных для пользователя с ИНН = itn.',
        request={'application/json': bool},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_update_moderated'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, itn):
        result = set_promo_data_moderated(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })


class UserRentedOutletsView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @extend_schema(
        description='Возвращает список торговых мест в арендном списке пользователя с ИНН = itn.',
        responses={
            (200, 'application/json'): oapi_result(fields.ListField(child=fields.CharField(), help_text='Список номеров торговых мест'), '_get_rents'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, itn):
        result = get_outlets_in_renting(DmUser.objects.get(aux_data__itn=itn))
        return Response({
            'result': result
        })

    @extend_schema(
        description='Помещает торговые места в арендный список пользователя с ИНН = itn. '
                    'В теле запроса передается список номеров торговых мест. '
                    'Статус торговых мест изменяется на RENTED.',
        request={'application/json': list[str]},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_post_rents'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, itn):
        result = rent_outlets(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Помещает торговые места в арендный список пользователя с ИНН = itn. '
                    'В теле запроса передается список номеров торговых мест. '
                    'Статус торговых мест изменяется на RENTED.',
        request={'application/json': list[str]},
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_put_rents'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, itn):
        result = rent_outlets(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Удаляет торговые места bp арендного списка пользователя с ИНН = itn. В теле запроса передается список номеров торговых мест. OpenAPI не позволяет вызвать этот метод.',
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_delete_rents'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, itn):
        result = unrent_outlets(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })


class NotificationsCRUDView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @extend_schema(
        description='Создает уведомления в Личном Кабинете. Если ИНН пользователя не указан в URL, создаются общие уведомления, иначе -- адресные.',
        request={'application/json': oapi_notification_serializer(True, '_post_notifications')},
        responses={
            (200, 'application/json'): oapi_result(fields.ListField(child=fields.IntegerField(), help_text='Список идентификаторов созданных сообщений'), '_post_notifications'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, itn=None):
        result = create_notifications(itn, request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Создает уведомления в Личном Кабинете. Если ИНН пользователя не указан в URL, создаются общие уведомления, иначе -- адресные.',
        request={'application/json': oapi_notification_serializer(True, '_put_notifications')},
        responses={
            (200, 'application/json'): oapi_result(fields.ListField(child=fields.IntegerField(), help_text='Список идентификаторов созданных сообщений'), '_put_notifications'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, itn=None):
        result = create_notifications(itn, request.data)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Возвращает существующие уведомления. Если ИНН пользователя не указан в URL, возвращаются общие уведомления, иначе -- адресные.',
        responses={
            (200, 'application/json'): oapi_result(oapi_notification_serializer(False, '_get_notifications'), '_get_notifications'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, itn=None):
        result = get_notifications(itn)
        return Response({
            'result': result
        })

    @extend_schema(
        description='Удаляет уведомления. Идентификаторы удаляемых уведомлений передаются в теле запроса как список целых. OpenAPI не позволяет вызвать этот метод.',
        responses={
            (200, 'application/json'): oapi_result(fields.BooleanField(help_text='Результат'), '_delete_notifications'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, itn=None):
        result = delete_notifications(itn, request.data)
        return Response({
            'result': result
        })


class SelfDiagnosisView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @extend_schema(
        description='Запускает процедуру диагностики и коррекции БД сайта. Результаты процедуры передаются в соответствующий метод API РД, см. Спецификации',
        responses={
            (200, 'application/json'): oapi_result(fields.CharField(help_text='Сообщение'), '_self_diagnosis'),
            (400, 'application/json'): OpenApiTypes.ANY,
        })
    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, _):
        if restore_db_consistency.launched():
            raise RuntimeWarning('Процедура диагностики выполняется, дождитесь её завершения')
        else:
            st_restore_db_consistency.delay()
            return Response({
                'result': 'Процедура диагностики запущена.'
            })


# TODO kill Dummy1C

@extend_schema(exclude=True)
class Dummy1C(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, operation):
        match operation:
            case 'confirmation':
                return Response(True)
            case 'booking':
                return Response(True)
            case 'regcard':
                return Response(True)
            case 'answers':
                return Response(True)
            case 'market-info':
                return Response(True)
            case 'moderation':
                return Response(True)
            case 'check':
                return Response(True)

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, _, operation):
        match operation:
            case 'confirmation':
                return Response(True)
            case 'booking':
                return Response(['000000000'])
            case 'regcard':
                return Response({
                    'Источник': 'API 1C',
                    'Параметр_1': 'Значение_1',
                    'Параметр_2': 'Значение_2',
                    'Параметр_3': 'Значение_3',
                    '...': '...',
                    'Параметр_N': 'Значение_N',
                })
            case 'answers':
                return Response(True)
            case 'market-info':
                return Response({
                    'Источник': 'API 1C',
                    'Параметр_1': 'Значение_1',
                    'Параметр_2': 'Значение_2',
                    'Параметр_3': 'Значение_3',
                    '...': '...',
                    'Параметр_N': 'Значение_N',
                })
            case 'moderation':
                return Response(True)
            case 'check':
                return Response(True)

    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, operation):
        match operation:
            case 'confirmation':
                return Response(True)
            case 'booking':
                return Response(['000000000'])
            case 'regcard':
                return Response(True)
            case 'answers':
                return Response(True)
            case 'market-info':
                return Response(True)
            case 'moderation':
                return Response(True)
            case 'check':
                return Response(True)
