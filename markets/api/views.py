from collections import OrderedDict
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponse
from markets.business.search_and_filters import apply_filter, filter_markets
from markets.business.actions import restore_db_consistency
from markets.decorators import on_exception_returns
from markets.models import SvgSchema, Market, TradePlaceType, TradeSpecType, TradePlace, TradeSector
from markets.tasks import st_restore_db_consistency
from redis import Redis
from .serializers import SchemeSerializer, TradePlaceTypeSerializer, TradeSpecTypeSerializer, TradePlaceSerializerO, TradePlaceSerializerS, TradeSectorSerializer, TradePlaceSerializerSec

try:  # To avoid deploy problems
    from transmutation import Svg3DTM
except ModuleNotFoundError:
    class Svg3DTM:
        pass

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


# -- Markets API ----------------------------------------------------------------------------------


class TakeMarketSchemesListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SchemeSerializer

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        market_pk = int(self.kwargs['market_pk'])
        market = Market.objects.get(pk=market_pk)
        return market.schemes.all()


# -- Scheme API --


class TakeSchemeGltfView(APIView):
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


class TakeSchemeSvgView(APIView):
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


class TakeSchemeOutletsStateView(APIView):
    permission_classes = [AllowAny]
    legends = ['trade_place_type_id', 'trade_spec_type_id_act_id', 'location_sector_id']

    @on_exception_returns(HttpResponseBadRequest, 'scheme_pk')
    def get(self, _, scheme_pk: int, legend: int):
        legend %= len(self.legends)
        leg_field = self.legends[legend]
        scheme = SvgSchema.objects.get(pk=scheme_pk)
        query = scheme.outlets.values('location_number', leg_field)
        return Response({str(r['location_number']): int(r[leg_field]) for r in query})

    @on_exception_returns(HttpResponseBadRequest, 'scheme_pk')
    def post(self, request, scheme_pk: int, legend: int):
        legend %= len(self.legends)
        leg_field = self.legends[legend]
        scheme = SvgSchema.objects.get(pk=scheme_pk)
        query = scheme.outlets.all()
        if request.data:
            for f_name, f_body in request.data.items():
                query = apply_filter(query, f_name, f_body)
        query = query.values('location_number', leg_field)
        return Response({str(r['location_number']): int(r[leg_field]) for r in query})


class TakeSchemeOutletsListView(ListAPIView):
    permission_classes = [AllowAny]
    legends = [TradePlaceSerializerO, TradePlaceSerializerS, TradePlaceSerializerSec]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        scheme_pk = int(self.kwargs['scheme_pk'])
        scheme = SvgSchema.objects.get(pk=scheme_pk)
        queryset = scheme.outlets.all()
        if self.request.data:
            for f_name, f_body in self.request.data.items():
                queryset = apply_filter(queryset, f_name, f_body)
        return queryset

    def get_serializer_class(self):
        legend = int(self.kwargs['legend']) % len(self.legends)
        return self.legends[legend]


# -- Info --

class TakeURLView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest)
    def post(request):
        data = request.data
        url = reverse(data['path_name'], kwargs=data['args'])
        return Response(url)


class TakeURLsView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest)
    def post(request):
        data = request.data
        market_pk = int(data['market_pk']) if 'market_pk' in data else None
        scheme_pk = int(data['scheme_pk']) if 'scheme_pk' in data else None
        legend = int(data['legend']) if 'legend' in data else None
        response = {}
        response |= {'url_market_schemes': reverse('api:markets_take_schemes', kwargs={'market_pk': market_pk})} \
            if market_pk is not None else {}
        response |= {'url_scheme_outlets_state': reverse('api:schemes_take_outlets_state', kwargs={'scheme_pk': scheme_pk, 'legend': legend})} \
            if scheme_pk is not None and legend is not None else {}
        response |= {'url_scheme_outlets_list': reverse('api:schemes_take_outlets_list', kwargs={'scheme_pk': scheme_pk, 'legend': legend})} \
            if scheme_pk is not None and legend is not None else {}
        response |= {'url_scheme_gltf': reverse('api:schemes_take_gltf', kwargs={'scheme_pk': scheme_pk})} \
            if scheme_pk is not None else {}
        response |= {'url_scheme_svg': reverse('api:schemes_take_svg', kwargs={'scheme_pk': scheme_pk})} \
            if scheme_pk is not None else {}
        response |= {'url_legend': reverse('api:info_take_legend', kwargs={'legend': legend})} \
            if legend is not None else {}
        return JsonResponse(response)


class TakeLegendView(ListAPIView):
    permission_classes = [AllowAny]
    legends = [
        {'title': 'По занятости',
         'model': TradePlaceType,
         'serializer_class': TradePlaceTypeSerializer},
        {'title': 'По специализации',
         'model': TradeSpecType,
         'serializer_class': TradeSpecTypeSerializer},
        {'title': 'По сектору',
         'model': TradeSector,
         'serializer_class': TradeSectorSerializer},
    ]

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, *args, **kwargs):
        legend = int(self.kwargs['legend']) % len(self.legends)
        return Response({
            'title': self.legends[legend]['title'],
            'legend': super().get(request, *args, **kwargs).data
        })

    def get_queryset(self):
        legend = int(self.kwargs['legend']) % len(self.legends)
        return self.legends[legend]['model'].objects.all()

    def get_serializer_class(self):
        legend = int(self.kwargs['legend']) % len(self.legends)
        return self.legends[legend]['serializer_class']


# -- Partial views --------------------------------------------------------------------------------


class PV_OutletTableView(APIView):
    permission_classes = [AllowAny]
    legends = [
        lambda o: o.trade_place_type.roof_color_css,
        lambda o: o.trade_spec_type_id_act.roof_color_css,
        lambda o: o.location_sector.roof_color_css,
    ]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, scheme_pk: int, legend: int):
        legend = legend % len(self.legends)
        scheme = SvgSchema.objects.get(pk=scheme_pk)
        queryset = scheme.outlets.all()
        if self.request.data:
            for f_name, f_body in self.request.data.items():
                queryset = apply_filter(queryset, f_name, f_body)
        outlets = [{
            'number': r.location_number,
            'specialization': r.trade_spec_type_id_act.type_name,
            'occupation': r.trade_place_type.type_name,
            'price': r.price,
            'color_css': self.legends[legend](r)
        } for r in queryset]
        return render(request, 'markets/partials/outlet-table.html', {
            'title': scheme.floor,
            'outlets': outlets,
            'hash': f'{hash((scheme_pk, legend))})'
        })


class PV_OutletDetailView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest, 'outlet_number')
    def post(self, request, outlet_number):
        return render(request, 'markets/partials/outlet-details.html', {
            'outlet': TradePlace.objects.get(location_number=outlet_number),
            'hash': f'{hash(outlet_number)}'
        })


class PV_FilteredMarketsView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request):
        markets = filter_markets(request.data['search_text'])
        context = OrderedDict()
        for m in markets:
            r = context.setdefault(m.geo_city.locality_name, OrderedDict()).setdefault(m.geo_district.locality_name, OrderedDict())
            r[m.mk_full_name] = {
                'address': f'{m.geo_street_type.type_name} {m.geo_street}{', ' if m.geo_house else ''}{m.geo_house}',
                'outlet_num': m.trade_places.count(),
                'link_map': reverse('markets:index'),
                'link_info': reverse('markets:market_details', kwargs={'mpk': m.id, 'show': 'info'}),
                'link_outlets': reverse('markets:market_details', kwargs={'mpk': m.id, 'show': 'outlets'}),
                'link_scheme': reverse('markets:market_details', kwargs={'mpk': m.id, 'show': 'scheme'}),
            }
        return render(request, 'markets/partials/filtered-markets.html', {'context': context})


class PV_HelpContentView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, hid: int):
        return render(request, f'markets/partials/help/help-{hid}', {'hid': hid})


# -- Actions --------------------------------------------------------------------------------------


class RestoreDatabaseConsistencyView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns(HttpResponseBadRequest)
    def get(_):
        if restore_db_consistency.launched():
            return Response({
                "status": "action in progress",
                "comment": "this is very, very long action, be patient, admin!"
            })
        else:
            st_restore_db_consistency.delay()
            return Response({
                "status": "launched in background",
                "comment": "this is very long action, be patient, please..."
            })

