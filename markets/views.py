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

    def get(self, request):
        return render(request, self.template_name, self.basic_context | {
            'markets': Market.objects.all()
        })


class ContactsView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/contacts.html'

    def get(self, request):
        return render(request, self.template_name, self.basic_context | {'text': 'Здесь будут контакты'})


class MarketDetailsView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/market-details.html'

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, mpk, show):
        return render(request, self.template_name, self.basic_context | {
            'market': Market.objects.get(pk=mpk)
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

#  Partials ---------------------------------------------------------------------------------------


class OutletDetailsPartialView(View):
    @property
    def template_name(self):
        return 'markets/partials/outlet-details.html'

    @on_exception_returns(HttpResponseBadRequest)
    def get(self, request, outlet_number):
        return render(request, self.template_name, {
            'outlet': TradePlace.objects.get(location_number=outlet_number)
        })
