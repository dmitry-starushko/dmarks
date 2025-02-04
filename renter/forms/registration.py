from django import forms
from django.core.exceptions import ValidationError
from markets.models import DmUser
from markets.validators import Validators
import re


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    sms_code = forms.CharField(initial='', label='Код подтверждения из СМС', required=False, widget=forms.HiddenInput)

    class Meta:
        model = DmUser
        fields = ['phone', 'first_name', 'last_name', 'email']

    def clean_phone(self):
        cd = self.cleaned_data
        try:
            Validators.phone(cd['phone'])
        except ValidationError:
            raise forms.ValidationError('Укажите номер телефона в формате +7(999)999-99-99')
        return cd['phone']

    def clean_password2(self):
        cd = self.cleaned_data
        password = cd['password2']
        if password != cd['password']:
            raise forms.ValidationError('Пароли не совпадают')
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать не менее 8 символов')
        if re.search('\\d', password) is None:
            raise forms.ValidationError('Пароль должен содержать хотя бы одну цифру')
        if re.search('[A-ZА-ЯЁ]', password) is None:
            raise forms.ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
        if re.search('[a-zа-яё]', password) is None:
            raise forms.ValidationError('Пароль должен содержать хотя бы одну строчную букву')
        return password
