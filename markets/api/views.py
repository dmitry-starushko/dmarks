from collections import OrderedDict
from django.conf import settings
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.urls import reverse, NoReverseMatch
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponse
from markets.business.search_and_filters import filter_markets, filter_outlets
from markets.decorators import on_exception_returns_response
from markets.models import SvgSchema, Market, TradePlaceType, TradeSpecType, TradePlace, TradeSector, GlobalObservation
from redis import Redis
from .serializers import TradePlaceTypeSerializer, TradeSpecTypeSerializer, TradeSectorSerializer
from ..business.booking import get_outlets_in_booking, BookingError, book_outlet, unbook_all
from ..enums import Observation, OutletState

try:  # To avoid deploy problems
    from transmutation import Svg3DTM
except ModuleNotFoundError:
    class Svg3DTM:
        pass

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


# -- Scheme API --

class TakeSchemeGltfView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns_response(HttpResponseBadRequest, 'scheme_pk')
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
    @on_exception_returns_response(HttpResponseBadRequest, 'scheme_pk')
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

    @on_exception_returns_response(HttpResponseBadRequest, 'scheme_pk')
    def get(self, _, scheme_pk: int, legend: int):
        legend %= len(self.legends)
        leg_field = self.legends[legend]
        scheme = SvgSchema.objects.defer('svg_schema').get(pk=scheme_pk)
        query = scheme.outlets.values('location_number', leg_field)
        return Response({str(r['location_number']): int(r[leg_field]) for r in query})

    @on_exception_returns_response(HttpResponseBadRequest, 'scheme_pk')
    def post(self, _, scheme_pk: int, legend: int):
        legend %= len(self.legends)
        leg_field = self.legends[legend]
        scheme = SvgSchema.objects.defer('svg_schema').get(pk=scheme_pk)
        query = scheme.outlets.all()
        query = query.values('location_number', leg_field)
        return Response({str(r['location_number']): int(r[leg_field]) for r in query})


# -- Info --

class TakeURLView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns_response(HttpResponseBadRequest)
    def post(request):
        data = request.data
        url = reverse(data['path_name'], kwargs=data['args'])
        return Response(url)


class TakeURLsView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @on_exception_returns_response(HttpResponseBadRequest)
    def post(request):
        data = request.data
        scheme_pk = int(data['scheme_pk']) if 'scheme_pk' in data else None
        legend = int(data['legend']) if 'legend' in data else None
        response = {}
        response |= {'url_scheme_outlets_state': reverse('api:schemes_take_outlets_state', kwargs={'scheme_pk': scheme_pk, 'legend': legend})} \
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

    @on_exception_returns_response(HttpResponseBadRequest)
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
    order_fields = ['location_number', 'trade_spec_type_id_act__type_name', 'trade_place_type__type_name', 'trade_type__type_name']
    column_count = len(order_fields)

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, scheme_pk: int, legend: int):
        order_map = {i: self.order_fields[i] for i in range(self.column_count)}
        ordering = []
        sorting_classes = {}
        match request.data:
            case str(params):
                params = params.strip()
                if params:
                    for chunk in params.split(','):
                        key, val = tuple(chunk.split(':', 1))
                        match int(key), val.strip():
                            case col, 'a' | 'A' if col in order_map:
                                ordering.append(order_map[col])
                                sorting_classes[f'sc_{col}'] = 'sort-asc'
                                order_map.pop(col)
                            case col, 'd' | 'D' if col in order_map:
                                ordering.append(f'-{order_map[col]}')
                                sorting_classes[f'sc_{col}'] = 'sort-desc'
                                order_map.pop(col)
                            case _: raise ValueError(f'Ошибка: {(key, val)}')
            case None: pass
            case _: raise ValueError(f'Недопустимый параметр: {request.data}')
        legend = legend % len(self.legends)
        scheme = SvgSchema.objects.defer('svg_schema').get(pk=scheme_pk)
        queryset = scheme.outlets.select_related('trade_place_type', 'trade_spec_type_id_act', 'trade_type').order_by(*ordering)
        outlets = [{
            'number': r.location_number,
            'specialization': r.trade_spec_type_id_act,
            'occupation': r.trade_place_type,
            'type': r.trade_type,
            'color_css': self.legends[legend](r)
        } for r in queryset]
        return render(request, 'markets/partials/outlet-table.html', {
            'title': scheme.floor,
            'outlets': outlets,
            'hash': f'{hash((scheme_pk, legend, ">".join(ordering)))})'
        } | sorting_classes)


class PV_OutletDetailView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns_response(HttpResponseBadRequest, 'outlet_number')
    def post(self, request, outlet_number):
        user = request.user
        outlet = TradePlace.objects.get(location_number=outlet_number)
        booked = get_outlets_in_booking(request.user)
        avail_for_booking = user.is_authenticated and (outlet.trade_place_type.type_name == OutletState.AVAILABLE_FOR_BOOKING) and (outlet_number not in booked)
        unbook = user.is_authenticated and len(booked) > 0
        return render(request, 'markets/partials/outlet-details.html', {
            'outlet': outlet,
            'afbk': avail_for_booking,
            'unbk': unbook,
            'hash': f'{hash(outlet_number) ^ hash(booked)}'
        })


class PV_FilteredMarketsView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns_response(HttpResponseBadRequest)
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
    joined_fields = ('market', 'trade_type', 'trade_place_type', 'trade_spec_type_id_act', 'market__geo_city', 'market__geo_district')

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request):
        context = OrderedDict()
        outlets = filter_outlets(request.data or None).select_related(*self.joined_fields)
        found = 0
        for o in outlets:
            try:
                r = (context.setdefault(o.market.geo_city.locality_name, OrderedDict()).setdefault(o.market.geo_district.locality_name, OrderedDict()).setdefault(o.market.mk_full_name, OrderedDict()))
                r[o.location_number] = {
                    'state': o.trade_place_type,
                    'specialization': o.trade_spec_type_id_act,
                    'price': o.price,
                    'type': o.trade_type,
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

    @on_exception_returns_response(HttpResponseBadRequest)
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

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, legend: int):
        legend = legend % len(self.legends)
        return render(request, 'markets/partials/legend-body.html', {
            'title': self.legends[legend]['title'],
            'legend': OrderedDict(self.legends[legend]['pairs']()),
        })


class PV_HelpContentView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, hid: int):
        try:
            return render(request, f'partials/help/help-{hid}.html', {'hid': hid, 'site_url': request.build_absolute_uri(reverse('markets:index'))})
        except TemplateDoesNotExist:
            return render(request, f'partials/help/help-0.html', {'hid': 0})


class PV_UserActionView(APIView):
    permission_classes = [IsAuthenticated]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request):
        render_message = lambda message: render(request, 'markets/partials/user/message.html', {'message': message})
        match request.data:
            # -- Бронирование ТМ --
            case {'action': 'book-outlet', 'outlet': str(number)}:
                try:
                    book_outlet(request.user, TradePlace.objects.get(location_number=number))
                    return render_message(f'Запрос на бронирование торгового места №{number} принят в обработку. Ожидайте уведомлений.')
                except BookingError as e:
                    return render_message(f'{e}')

            # -- Отмена бронирований --
            case {'action': 'unbook-all'}:
                unbooked = unbook_all(request.user)
                return render_message(f'Отменена заявка на бронирование торговых мест {', '.join(unbooked)}' if unbooked else 'Ни одна заявка на бронирование не была отменена')

            # -- Что-то вне списка реализованных акций --
            case _: return render_message('К сожалению, данная операция еще не реализована. Обратитесь к службе технической поддержке сайта.')
