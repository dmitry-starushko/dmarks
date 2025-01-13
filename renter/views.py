from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from renter.forms.business_card import BusinessCardForm
from renter.forms.registration import RegistrationForm


class RenterView(LoginRequiredMixin, View):
    @property
    def template_name(self):
        return 'renter/renter.html'

    def get(self, request):
        user = request.user
        chunks = f'{user.aux_data.promo_text}'.split('\n\n', 1) if user.confirmed else []
        slogan = chunks[0] if chunks else ''
        other_text = chunks[1] if len(chunks) > 1 else ''
        business_card = {
            'business_card': BusinessCardForm(initial={
                'slogan': slogan,
                'promo_text': other_text
            })
        } if user.confirmed else {}
        parm_msg = request.GET.get('message', None)
        message = {
            'message': urlsafe_base64_decode(parm_msg).decode('utf-8')
        } if parm_msg is not None else {}
        return render(request, self.template_name, {
            'user': user,
            'help_id': 400,
        } | business_card | message)

    def post(self, request):
        business_card = BusinessCardForm(request.POST, request.FILES)
        if business_card.is_valid():
            user = request.user
            if user.confirmed:
                cd = business_card.cleaned_data
                pimg = request.FILES['promo_image']
                with transaction.atomic():
                    user.aux_data.promo_text = '\n\n'.join([cd['slogan'], cd['promo_text']])
                    user.aux_data.promo_image.save(pimg.name, pimg)
                    user.aux_data.save()
        return redirect('renter:renter')


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

