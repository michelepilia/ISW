from django import forms
from IswBus import models
from datetime import datetime
from IswBus.models import CartaDiCredito
from django.contrib.auth.models import User

now = datetime.now()


class CardModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()


class CreditCardForm(forms.Form):
    card_number = forms.CharField(label="Numero Carta di Credito", max_length=16)
    expiration_month = forms.IntegerField(label="Mese di Scadenza", min_value=1, max_value=12)
    expiration_year = forms.IntegerField(label="Anno di Scadenza", min_value=datetime.now().year)
    cvv = forms.CharField(label="Codice CVV", max_length=3)


class BuyTicketForm(forms.Form):
    carta = CardModelChoiceField(queryset=CartaDiCredito.objects.none(), label='Seleziona carta')

    def __init__(self, request, *args, **kwargs):
        super(BuyTicketForm, self).__init__(*args, **kwargs)
        if request.user:
            queryset = CartaDiCredito.objects.filter(user_id=request.user.id)
        else:
            queryset = CartaDiCredito.objects.none()
        self.fields['carta'].queryset = queryset


