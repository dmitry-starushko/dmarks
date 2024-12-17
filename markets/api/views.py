from collections import OrderedDict
from django.conf import settings
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.urls import reverse, NoReverseMatch
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponse
from markets.business.search_and_filters import apply_filter, filter_markets, filter_outlets
from markets.business.actions import restore_db_consistency
from markets.decorators import on_exception_returns
from markets.models import SvgSchema, Market, TradePlaceType, TradeSpecType, TradePlace, TradeSector, GlobalObservation
from markets.tasks import st_restore_db_consistency
from redis import Redis
from .serializers import SchemeSerializer, TradePlaceTypeSerializer, TradeSpecTypeSerializer, TradePlaceSerializerO, TradePlaceSerializerS, TradeSectorSerializer, TradePlaceSerializerSec
from ..enums import Observation

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
        queryset = scheme.outlets.select_related('trade_place_type', 'trade_spec_type_id_act')
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
        context = OrderedDict()
        markets = filter_markets(request.data['search_text']).select_related('geo_city', 'geo_district', 'geo_street_type')
        for m in markets:
            r = context.setdefault(m.geo_city.locality_name, OrderedDict()).setdefault(m.geo_district.locality_name, OrderedDict())
            r[m.mk_full_name] = {
                'address': f'{m.geo_street_type.type_name} {m.geo_street}{', ' if m.geo_house else ''}{m.geo_house}',
                'outlet_num': m.trade_places.count(),
                'link_map': reverse('markets:index_mpk', kwargs={'mpk': m.id}),
                'link_info': reverse('markets:market_details', kwargs={'mpk': m.id, 'show': 'info'}),
                'link_outlets': reverse('markets:market_details', kwargs={'mpk': m.id, 'show': 'outlets'}),
                'link_scheme': reverse('markets:market_details', kwargs={'mpk': m.id, 'show': 'scheme'}),
            }
        return render(request, 'markets/partials/filtered-markets.html', {'context': context})


class PV_FilteredOutletsView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request):
        context = OrderedDict()
        outlets = filter_outlets(request.data or None).select_related('market', 'trade_place_type', 'trade_spec_type_id_act', 'market__geo_city', 'market__geo_district')
        found = 0
        for o in outlets:
            try:
                r = (context.setdefault(o.market.geo_city.locality_name, OrderedDict()).setdefault(o.market.geo_district.locality_name, OrderedDict()).setdefault(o.market.mk_full_name, OrderedDict()))
                r[o.location_number] = {
                    'state': o.trade_place_type,
                    'specialization': o.trade_spec_type_id_act,
                    'price': o.price,
                    'link_outlets': reverse('markets:market_details_outlet', kwargs={'mpk': o.market.id, 'show': 'outlets', 'outlet': o.location_number}),
                    'link_scheme': reverse('markets:market_details_outlet', kwargs={'mpk': o.market.id, 'show': 'scheme', 'outlet': o.location_number}),
                }
                found += 1
            except NoReverseMatch as e:
                print(e)
        return render(request, 'markets/partials/filtered-outlets.html', {
            'context': context,
            'found': found
        })


class PV_OutletFiltersView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, full):
        locations = OrderedDict()
        if full:
            related_fields = ['geo_city', 'geo_district', 'geo_street_type']
            order_fields = ['geo_city__locality_name', 'geo_district__locality_name', 'market_name', 'additional_name']
            for m in Market.objects.select_related(*related_fields).order_by(*order_fields):
                r = locations.setdefault(m.geo_city.locality_name, OrderedDict()).setdefault(m.geo_district.locality_name, OrderedDict())
                r[m.mk_full_name] = m.id
        occupation_types = OrderedDict((str(t), t.id) for t in TradePlaceType.objects.order_by('type_name'))
        specializations = OrderedDict((str(t), t.id) for t in TradeSpecType.objects.order_by('type_name'))
        facilities = OrderedDict([
            ('Выносная торговля', 'street_vending'),
            ('Электричество', 'impr_electricity'),
            ('Теплоснабжение', 'impr_heat_supply'),
            ('Кондиционирование', 'impr_air_conditioning'),
            ('Водопровод', 'impr_plumbing'),
            ('Канализация', 'impr_sewerage'),
            ('Стоки', 'impr_drains'),
            ('Интернет', 'impr_internet'),
            ('Стенды, мебель', 'impr_add_equipment'),
            ('Холодильники', 'impr_fridge'),
            ('Витрины', 'impr_shopwindow')
        ])
        p_min = GlobalObservation.objects.get_or_create(key=Observation.OUTLET_RENTING_COST_MIN)[0].decimal
        p_max = GlobalObservation.objects.get_or_create(key=Observation.OUTLET_RENTING_COST_MAX)[0].decimal
        price_range = {
            'min': p_min,
            'max': p_max if p_min < p_max else p_min + 1000
        }
        a_min = GlobalObservation.objects.get_or_create(key=Observation.OUTLET_AREA_MIN)[0].decimal
        a_max = GlobalObservation.objects.get_or_create(key=Observation.OUTLET_AREA_MAX)[0].decimal
        area_range = {
            'min': a_min,
            'max': a_max if a_min < a_max else a_min + 1000
        }
        return render(request, 'markets/partials/outlet-filters.html', {
            'full': not not full,
            'locations': locations,
            'specializations': specializations,
            'occupation_types': occupation_types,
            'facilities': facilities,
            'price_range': price_range,
            'area_range': area_range
        })


class PV_LegendBodyView(APIView):
    permission_classes = [AllowAny]

    legends = [
        {'title': 'По занятости',
         'pairs': lambda: ((r, r.roof_color_css) for r in TradePlaceType.objects.order_by('type_name'))},
        {'title': 'По специализации',
         'pairs': lambda: ((r, r.roof_color_css) for r in TradeSpecType.objects.order_by('type_name'))},
        {'title': 'По секторам',
         'pairs': lambda: ((r, r.roof_color_css) for r in TradeSector.objects.order_by('sector_name'))},
    ]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, legend: int):
        legend = legend % len(self.legends)
        return render(request, 'markets/partials/legend-body.html', {
            'title': self.legends[legend]['title'],
            'legend': OrderedDict(self.legends[legend]['pairs']()),
        })


class PV_HelpContentView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns(HttpResponseBadRequest)
    def post(self, request, hid: int):
        try:
            return render(request, f'markets/partials/help/help-{hid}.html', {'hid': hid})
        except TemplateDoesNotExist:
            return render(request, f'markets/partials/help/help-0.html', {'hid': 0})


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

