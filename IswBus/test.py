import unittest

from django.contrib.auth import authenticate
from django.test import TestCase, Client, TransactionTestCase
from IswBus.models import *
from datetime import datetime
from django.db import transaction
from IswBus.forms import *
from django.db import models, IntegrityError


#Test sulla creazione dei biglietti
class BigliettoTest(TransactionTestCase):

    def setUp(self):

        #Creazione biglietti
        dodiciCorse = Biglietto(nome='dodiciCorse', validitaGiorni=10, costo=2.00, tipologia='3')

        #Salvataggio biglietti
        dodiciCorse.save()

        self.dodici = dodiciCorse
        self.obj_count = Biglietto.objects.all().count()

    #Controllo numero di biglietti creati
    def testTicketCount(self):                                
        self.assertEqual(self.obj_count, 1)


#Test sulla creazione delle carte di credito
class CartaDiCreditoTest(TransactionTestCase):

    def setUp(self):
        self.c = Client()

        user_data = {'username': 'studente', 'password1': '12345678pw', 'password2': '12345678pw'}
        self.client.post('/signup/', user_data)

        login_data = {'username': 'studente', 'password': '12345678pw'}
        self.response= self.client.post('/login/', login_data, follow=True)
        self.user = self.response.context['user']

        #Creazione carte di credito corrette
        mastercardPilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=2021, cvv='123', user=self.user)
        mastercardPilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2022, cvv='321', user=self.user)

        #Creazione carta di credito errata (viola vincolo unique)
        mastercardPiliaErrata = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2015, cvv='421', user=self.user)

        #Salvataggio carte
        mastercardPilia.save()
        mastercardPilia2.save()

        #Test sull'aggiunta della carta errata
        try:
            mastercardPiliaErrata.save()
        except IntegrityError:
            pass

        self.obj_num = CartaDiCredito.objects.all().count()
        self.card1 = mastercardPilia
        self.card2 = mastercardPilia2

    #Test sul numero delle carte di credito
    def testUnitCardNumber(self):
        self.assertEqual(len(CartaDiCredito.objects.all()), 2)
