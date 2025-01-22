from django.conf import settings
from django.http import HttpResponseBadRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import fields
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from extapi.openapi import oapi_market_serializer, oapi_result
from markets.business.confirmation import set_user_confirmed
from markets.business.crud_entities import create_market, update_market, get_market, delete_market, create_market_outlets, get_market_outlets, update_market_outlets, delete_market_outlets, \
    create_market_schemes, get_market_schemes, update_market_schemes, delete_market_schemes, create_market_images, get_market_images, update_market_images, delete_market_images, create_market_phones, \
    get_market_phones, update_market_phones, delete_market_phones, create_market_emails, get_market_emails, update_market_emails, delete_market_emails, create_notifications, get_notifications, \
    delete_notifications
from markets.business.moderation import set_promo_data_moderated
from markets.business.renting import rent_outlets, get_outlets_in_renting, unrent_outlets
from markets.decorators import on_exception_returns_response
from markets.models import DmUser


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

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, mid):
        result = create_market_outlets(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, mid):
        result = get_market_outlets(mid)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, mid):
        result = update_market_outlets(mid, request.data)
        return Response({
            'result': result
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

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, itn):
        result = set_user_confirmed(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, itn):
        result = set_user_confirmed(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, itn):
        result = DmUser.objects.get(aux_data__itn=itn).confirmed
        return Response({
            'result': result
        })


class UserRentedOutletsView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, itn):
        result = rent_outlets(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, itn):
        result = get_outlets_in_renting(DmUser.objects.get(aux_data__itn=itn))
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, itn):
        result = rent_outlets(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, itn):
        result = unrent_outlets(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })


class UserModeratedView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, itn):
        result = set_promo_data_moderated(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, itn):
        result = set_promo_data_moderated(DmUser.objects.get(aux_data__itn=itn), request.data)
        return Response({
            'result': result
        })


class NotificationsCRUDView(APIView):
    permission_classes = settings.EXT_API_PERMISSIONS

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, itn=None):
        result = create_notifications(itn, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, itn=None):
        result = get_notifications(itn)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, itn=None):
        result = delete_notifications(itn, request.data)
        return Response({
            'result': result
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

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, operation):
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
