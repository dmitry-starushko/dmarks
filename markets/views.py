from django.views import View
from django.shortcuts import render

from markets.models import Market


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

    def get(self, request, mpk, show):
        return render(request, self.template_name, self.basic_context | {
            'market': Market.objects.get(pk=mpk)
        })
