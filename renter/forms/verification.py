from django import forms


class VerificationForm(forms.Form):
    itn = forms.CharField(label='ИНН', min_length=10, max_length=12)
    usr_le_extract = forms.FileField(label='Скан выписки из ЕСГРЮЛ')
    passport_scan = forms.FileField(label='Скан паспорта')
