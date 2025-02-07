from django import forms
from django.core.exceptions import ValidationError
from markets.models import DmUser
from markets.validators import Validators
import re


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    confirm = forms.BooleanField(initial=False, label='Я соглашаюсь с политикой конфиденциальности данного сайта')
    sms_code = forms.CharField(initial='', label='Введите код подтверждения из SMS', required=False, widget=forms.HiddenInput)

    class Meta:
        model = DmUser
        fields = ['phone', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in {'phone': 'Телефон', 'email': 'Адрес электронной почты'}.items():
            self.fields[key].label = val

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        try:
            Validators.phone(phone)
        except ValidationError:
            raise forms.ValidationError('Укажите номер телефона в формате +7(999)999-99-99')
        return phone

    def clean_confirm(self):
        confirm = self.cleaned_data['confirm']
        if not confirm:
            raise forms.ValidationError('Ваше согласие необходимо для регистрации')
        return confirm

    def clean_password2(self):
        cd = self.cleaned_data
        password = cd['password2']
        if password != cd['password']:
            raise forms.ValidationError('Пароли не совпадают')
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать не менее 8 символов')
        if re.search(r'\d', password) is None:
            raise forms.ValidationError('Пароль должен содержать хотя бы одну цифру')
        if re.search(r'[A-ZА-ЯЁ]', password) is None:
            raise forms.ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
        if re.search(r'[a-zа-яё]', password) is None:
            raise forms.ValidationError('Пароль должен содержать хотя бы одну строчную букву')
        return password
