from collections import OrderedDict
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest
from django.views import View
from django.shortcuts import render
from markets.business.aux_info import get_market_info
from markets.decorators import on_exception_returns_response
from markets.models import Market, Contact


class BasicContextProvider:
    def basic_context(self, request, model=None):
        return {
            'page_title': f'{self.pg_title(model)}',
            'og_description': f'{self.og_description(model)}',
            'og_image': f'{settings.SITE_ROOT}{self.og_image(model)}',
            'pg_canonical': f'{settings.SITE_ROOT}/{self.pg_canonical(model)}',
            'body_class': 'index-page',
            'user': request.user,
        }

    def pg_title(self, _):
        return ''

    def og_description(self, _):
        return f'Цифровая информационная система интерактивных карт территорий рынков ГП «Рынки Донбасса». Онлайн бронирование торговых мест'

    def og_image(self, _):
        return default_storage.url(settings.DEF_MK_IMG)

    def pg_canonical(self, _):
        return ''


class IndexView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/index.html'

    def pg_title(self, _):
        return 'ЦИС интерактивных карт территорий рынков ГП «Рынки Донбасса»'

    def get(self, request, mpk: int | None = None):
        return render(request, self.template_name, self.basic_context(request) | {
            'markets': Market.objects.all(),
            'mpk': int(mpk) if mpk is not None else 0,
            'help_id': 100,
        })


class MarketDetailsView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/market-details.html'

    def pg_title(self, market_model):
        return f'{market_model.mk_full_name} ({market_model.market_type}). Рынки Донбасса'

    def og_description(self, market_model):
        return f'Онлайн бронирование торговых мест {market_model.mk_full_name} ({market_model.market_type}), {market_model.geo_city}'

    def og_image(self, market_model):
        return default_storage.url(market_model.image)

    def pg_canonical(self, market_model):  # TODO use reverse() instead f-string
        return f'market-detail/{market_model.id}/info/'

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, mpk, show: str, outlet: str | None = None):
        market_model = Market.objects.get(pk=mpk)
        outlet_model = market_model.trade_places.get(location_number=str(outlet)) if outlet is not None else None
        return render(request, self.template_name, self.basic_context(request, market_model) | {
            'market': market_model,
            'aux_info': get_market_info(market_model.market_id),
            'show_tab': show,
            'outlet': outlet_model,
            'help_id': 200,
        })


class ContactsView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/contacts.html'

    def pg_title(self, _):
        return 'Контакты. ЦИС интерактивных карт территорий рынков'

    def pg_canonical(self, _):  # TODO use reverse() instead direct string
        return 'contacts/'

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request):
        data = OrderedDict()
        contacts = Contact.objects.select_related('city', 'district')
        for c in contacts:
            r = data.setdefault(c.city.locality_name, OrderedDict()).setdefault(c.district.locality_name, OrderedDict())
            r[c.id] = c
        return render(request, self.template_name, self.basic_context(request) | {
            'data': data,
            'help_id': 300,
        })
