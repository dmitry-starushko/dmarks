from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from markets.business.logging import dlog_info
from markets.tasks import st_moderate_promo_data
from renter.forms.business_card import BusinessCardForm
from renter.forms.registration import RegistrationForm
from django.contrib.auth import views as auth_views, forms as auth_forms
from django import forms as dj_forms
from renter.sms import send_sms_code, check_sms_code


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
                    user.aux_data.promo_enabled = False
                    user.aux_data.save()
                    st_moderate_promo_data.delay(user.itn)
                dlog_info(user, f'Пользователь {user.phone} изменил данные визитной карточки; инициирована модерация')
        return redirect('renter:renter')


class AuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Телефон'


class LoginView(auth_views.LoginView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authentication_form = AuthenticationForm


class RegistrationView(View):
    COOKIE_NAME = 'dm_sms_code_uuid'

    @property
    def template_name(self):
        return 'registration/register.html'

    def get(self, request):
        form = RegistrationForm()
        response = render(request, self.template_name, {'form': form})
        response.delete_cookie(self.COOKIE_NAME)
        return response

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if (sms_code_uuid := request.COOKIES.get(self.COOKIE_NAME, '@')) == '@':
                sms_code_uuid = send_sms_code(form.cleaned_data['phone'])
            sms_code = form.cleaned_data['sms_code']
            if not (sms_code and check_sms_code(sms_code, sms_code_uuid)):
                for f in ('phone', 'email', 'first_name', 'last_name', 'password', 'password2', 'confirm'):
                    form.fields[f].widget = dj_forms.HiddenInput()
                form.fields['sms_code'].widget = dj_forms.TextInput()
                response = render(request, self.template_name, {'form': form})
                response.set_cookie(self.COOKIE_NAME, sms_code_uuid)
                return response
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'user': new_user})
        else:
            return render(request, self.template_name, {'form': form})

