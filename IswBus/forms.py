from django import forms
from IswBus import models
from datetime import datetime
from IswBus.models import CartaDiCredito

now = datetime.now()


class CardModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()


class CreditCardForm(forms.Form):
    card_number = forms.CharField(label="Numero Carta di Credito", max_length=16)
    expiration_month = forms.IntegerField(label="Mese di Scadenza", min_value=1, max_value=12)
    expiration_year = forms.IntegerField(label="Anno di Scadenza", min_value=now.year)
    cvv = forms.CharField(label="Codice CVV", max_length=3)



class UserForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=50)
    cognome = forms.CharField(label="Cognome", max_length=50)


class BuyTicketForm(forms.Form):
    carta = forms.ModelChoiceField(queryset = CartaDiCredito.objects.all())