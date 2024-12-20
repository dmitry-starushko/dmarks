from django.http import HttpResponseBadRequest
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from ..business.crud_entities import create_market, update_market, get_market, delete_market
from ..decorators import on_exception_returns


class MarketCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, mid):
        result = create_market(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, mid):
        result = get_market(mid)
        return Response({
            'result': result
        })

    @on_exception_returns(HttpResponseBadRequest)
    def put(self, request, mid):
        result = update_market(mid, request.data)
        return Response({
            'result': result
        })

    @on_exception_returns(HttpResponseBadRequest)
    def delete(self, request, mid):
        result = delete_market(mid)
        return Response({
            'result': result
        })


class MarketOutletsCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def put(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def delete(self, request, mid):
        pass


class MarketSchemesCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def put(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def delete(self, request, mid):
        pass


class MarketImagesCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def put(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def delete(self, request, mid):
        pass


class MarketPhonesCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def put(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def delete(self, request, mid):
        pass


class MarketEmailsCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def put(self, request, mid):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def delete(self, request, mid):
        pass


class UserCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, phone):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, phone):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def put(self, request, phone):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def delete(self, request, phone):
        pass


class UserOutletsCRUDView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, phone):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, phone):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def put(self, request, phone):
        pass

    @on_exception_returns(HttpResponseBadRequest)
    def delete(self, request, phone):
        pass
