from django import forms
from IswBus import models

class CreditCardForm(forms.Form):
    quantita = forms.IntegerField('Numero biglietti',min_value=1, max_value=10)
    cartaDiCredito = forms.ModelChoiceField(queryset=models.CartaDiCredito.objects.all())