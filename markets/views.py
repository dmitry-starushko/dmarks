from django.views import View
from django.shortcuts import render


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
        return render(request, self.template_name, self.basic_context)


class ContactsView(View, BasicContextProvider):
    @property
    def template_name(self):
        return 'markets/contacts.html'

    def get(self, request):
        return render(request, self.template_name, self.basic_context | {'page_title': 'Здесь будут контакты'})
