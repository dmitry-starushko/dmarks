from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponse
from markets.decorators import on_exception_returns
from markets.models import SvgSchema

try:
    from transmutation import Svg3DTM
except ModuleNotFoundError:
    class Svg3DTM:
        def __init__(self):
            raise RuntimeError("The transmutation library isn't plugged in")


class TakeGltfView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest)
    def get(_, scheme_pk: int):
        scheme = SvgSchema.objects.get(pk=scheme_pk)
        svg3dtm = Svg3DTM()
        response = JsonResponse({})
        response.content = svg3dtm.transmutate(scheme.svg_schema)
        return response


class TakeSvgView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest)
    def get(_, scheme_pk: int):
        scheme = SvgSchema.objects.get(pk=scheme_pk)
        response = HttpResponse()
        response.content = scheme.svg_schema
        return response


class TakeOutletsView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest)
    def get(_, scheme_pk: int):
        scheme = SvgSchema.objects.get(pk=scheme_pk)
        query = scheme.market.trade_places.values('location_number', 'trade_place_type_id')
        return Response({
            str(r['location_number']): int(r['trade_place_type_id']) for r in query
        })
