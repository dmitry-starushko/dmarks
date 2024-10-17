from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http.response import JsonResponse, HttpResponseBadRequest
from markets.decorators import on_exception_returns
from markets.models import SvgSchema
from transmutation import Svg3DTM


class TakeGltfView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest)
    def get(request, scheme_pk: int):
        scheme = SvgSchema.objects.get(pk=scheme_pk)
        svg3dtm = Svg3DTM()
        r = JsonResponse({})
        r.content = svg3dtm.transmutate(scheme.svg_schema)
        return r


