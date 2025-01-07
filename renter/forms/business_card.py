from django import forms


class BusinessCardForm(forms.Form):
    slogan = forms.CharField(label='Слоган', min_length=3, required=True, widget=forms.TextInput(attrs={'placeholder': 'Слоган'}))
    promo_text = forms.CharField(label='Промо-текст', min_length=3, required=True, widget=forms.Textarea())
    promo_image = forms.FileField(label='Промо-изображение', required=True, widget=forms.FileInput(attrs={'accept': 'image/*'}))
