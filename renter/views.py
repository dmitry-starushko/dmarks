from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class RenterView(LoginRequiredMixin, View):
    @property
    def template_name(self):
        return 'renter/renter.html'

    def get(self, request):
        return render(request, self.template_name, {
            'user': request.user
        })
