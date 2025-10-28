from django import forms

class PeselForm(forms.Form):
    pesel = forms.CharField(
        label='Numer PESEL',
        max_length=11,
        min_length=11,
        widget=forms.TextInput(attrs={'placeholder': 'Wpisz numer PESEL'})
    )