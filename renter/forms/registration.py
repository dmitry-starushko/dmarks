from django import forms
from markets.models import DmUser


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = DmUser
        fields = ['phone', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data()
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
