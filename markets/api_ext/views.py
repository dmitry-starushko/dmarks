from django.http import HttpResponseBadRequest
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from ..business.crud_entities import create_market, update_market, get_market, delete_market, create_market_outlets, get_market_outlets, update_market_outlets, delete_market_outlets, \
    create_market_schemes, get_market_schemes, update_market_schemes, delete_market_schemes, create_market_images, get_market_images, update_market_images, delete_market_images, create_market_phones, \
    get_market_phones, update_market_phones, delete_market_phones, create_market_emails, get_market_emails, update_market_emails, delete_market_emails
from ..decorators import on_exception_returns_response


class MarketCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, mid):
        result = create_market(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, mid):
        result = get_market(mid)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, mid):
        result = update_market(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, mid):
        result = delete_market(mid)
        return Response({
            'result': result
        })


class MarketOutletsCRUDView(APIView):
    permission_classes = [AllowAny]

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


class MarketSchemesCRUDView(APIView):
    permission_classes = [AllowAny]

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


class MarketImagesCRUDView(APIView):
    permission_classes = [AllowAny]

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


class MarketPhonesCRUDView(APIView):
    permission_classes = [AllowAny]

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


class MarketEmailsCRUDView(APIView):
    permission_classes = [AllowAny]

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


class UserCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, phone):
        pass

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, phone):
        pass

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, phone):
        pass

    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, phone):
        pass


class UserOutletsCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, phone):
        pass

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, phone):
        pass

    @on_exception_returns_response(HttpResponseBadRequest)
    def put(self, request, phone):
        pass

    @on_exception_returns_response(HttpResponseBadRequest)
    def delete(self, request, phone):
        pass
