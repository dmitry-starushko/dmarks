from threading import Thread
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponse
from markets.api.business import restore_db_consistency
from markets.decorators import on_exception_returns
from markets.models import SvgSchema
from redis import Redis

try:
    from transmutation import Svg3DTM
except ModuleNotFoundError:
    class Svg3DTM:
        def __init__(self):
            raise RuntimeError("The transmutation library isn't plugged in")

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class TakeGltfView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest, 'scheme_pk')
    def get(_, scheme_pk: int):
        key = f'scheme:{scheme_pk}:gltf'
        if (gltf := redis.get(key)) is None:
            scheme = SvgSchema.objects.get(pk=scheme_pk)
            svg3dtm = Svg3DTM()
            gltf = svg3dtm.transmutate(scheme.svg_schema)
            redis.set(name=key, value=gltf, ex=settings.SCHEME_EXPIRE_SECONDS)
        response = JsonResponse({})
        response.content = gltf
        return response


class TakeSvgView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest, 'scheme_pk')
    def get(_, scheme_pk: int):
        key = f'scheme:{scheme_pk}:svg'
        if (svg := redis.get(key)) is None:
            svg = SvgSchema.objects.get(pk=scheme_pk).svg_schema
            redis.set(name=key, value=svg, ex=settings.SCHEME_EXPIRE_SECONDS)
        response = HttpResponse()
        response.content = svg
        return response


class TakeOutletsView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest, 'scheme_pk')
    def get(_, scheme_pk: int):
        scheme = SvgSchema.objects.get(pk=scheme_pk)
        query = scheme.market.trade_places.filter(location_floor=int(scheme_pk)).values('location_number', 'trade_place_type_id')
        return Response({
            str(r['location_number']): int(r['trade_place_type_id']) for r in query
        })


class RestoreDatabaseConsistencyView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest)
    def get(_):
        if restore_db_consistency.launched():
            return Response({
                "status": "action in progress",
                "comment": "this is very, very long action, be patient, admin!"
            })
        else:
            thread = Thread(target=restore_db_consistency, args=(), daemon=True)
            thread.start()
            return Response({
                "status": "launched",
                "comment": "this is very long action, be patient, please..."
            })

