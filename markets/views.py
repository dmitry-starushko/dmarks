from django.views import View
from django.shortcuts import render


class IndexView(View):
    @property
    def template_name(self):
        return 'markets/index.html'

    def get(self, request):
        return render(request, self.template_name, {
            'page_title': 'Рынки Донбасса',
            'body_class': 'index-page',
        })

