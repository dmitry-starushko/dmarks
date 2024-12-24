from collections import OrderedDict
from django.http import HttpResponseBadRequest
from django.views import View
from django.shortcuts import render
from markets.decorators import on_exception_returns_response
from markets.models import Market, Contact


class BasicContextProvider:
    @property
    def basic_context(self):
        return {
            'page_title': 'Рынки Донбасса',
            'body_class': 'index-page',
        }


class IndexView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/index.html'

    def get(self, request, mpk: int | None = None):
        return render(request, self.template_name, self.basic_context | {
            'markets': Market.objects.all(),
            'mpk': int(mpk) if mpk is not None else 0,
            'help_id': 100,
        })


class MarketDetailsView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/market-details.html'

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, mpk, show: str, outlet: str | None = None):
        market_model = Market.objects.get(pk=mpk)
        outlet_model = market_model.trade_places.get(location_number=str(outlet)) if outlet is not None else None
        return render(request, self.template_name, self.basic_context | {
            'market': market_model,
            'show_tab': show,
            'outlet': outlet_model,
            'help_id': 200,
        })


class ContactsView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/contacts.html'

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request):
        data = OrderedDict()
        contacts = Contact.objects.select_related('city', 'district')
        for c in contacts:
            r = data.setdefault(c.city.locality_name, OrderedDict()).setdefault(c.district.locality_name, OrderedDict())
            r[c.id] = c
        return render(request, self.template_name, {
            'data': data,
            'help_id': 300,
        })


class Scheme3DView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/scheme3d.html'

    @on_exception_returns_response(HttpResponseBadRequest)
    def get(self, request, scheme_pk):
        return render(request, self.template_name, self.basic_context | {
            'scheme_pk': scheme_pk
        })
