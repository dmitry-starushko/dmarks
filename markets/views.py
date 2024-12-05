from django.http import HttpResponseBadRequest
from django.views import View
from django.shortcuts import render
from markets.decorators import on_exception_returns
from markets.models import Market, TradePlace


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

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, mpk, show):
        return render(request, self.template_name, self.basic_context | {
            'market': Market.objects.get(pk=mpk),
            'show_tab': show,
            'help_id': 200,
        })


class ContactsView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/contacts.html'

    def get(self, request):
        return render(request, self.template_name, self.basic_context | {
            'text': 'Здесь будут контакты',
            'help_id': 300,
        })


class Scheme3DView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/scheme3d.html'

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, scheme_pk):
        return render(request, self.template_name, self.basic_context | {
            'scheme_pk': scheme_pk
        })
