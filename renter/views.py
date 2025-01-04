from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from renter.forms.registration import RegistrationForm


class RenterView(LoginRequiredMixin, View):
    @property
    def template_name(self):
        return 'renter/renter.html'

    def get(self, request):
        return render(request, self.template_name, {
            'user': request.user
        })


class RegistrationView(View):
    @property
    def template_name(self):
        return 'registration/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': RegistrationForm()})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'user': new_user})
        else:
            return render(request, self.template_name, {'form': form})

