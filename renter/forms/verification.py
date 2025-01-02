from django import forms
from markets.validators import Validators


class VerificationForm(forms.Form):
    itn = forms.CharField(label='ИНН', min_length=10, max_length=12, required=True, validators=[Validators.itn], widget=forms.TextInput(attrs={'pattern': Validators.ITN, 'placeholder': 'Число из 10 или 12 цифр'}))
    usr_le_extract = forms.FileField(label='Скан выписки из ЕСГРЮЛ', max_length=1024, required=True, widget=forms.FileInput(attrs={'accept': 'image/*,.pdf'}))
    passport_scan = forms.FileField(label='Скан паспорта', required=True, widget=forms.FileInput(attrs={'accept': 'image/*,.pdf'}))
