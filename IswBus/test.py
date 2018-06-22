import unittest

from django.contrib.auth import authenticate
from django.test import TestCase, Client, TransactionTestCase
from IswBus.models import *
from datetime import datetime
from django.db import transaction

from IswBus.forms import *
from django.db import models, IntegrityError

class ModelTest(TransactionTestCase):
    def setUp(self):
        user = User(username='mario', password='gatto')
        user.save()

        dodiciCorse = Biglietto(nome='dodiciCorse', validitaGiorni=10, costo=2.00, tipologia='3')
        dodiciCorse.save()


        mastercardPilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=21, cvv='123', user=user)
        mastercardPilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=22, cvv='321', user=user)



        mastercardPiliaErrata = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=15, cvv='421', user=user)
        mastercardPilia.save()
        mastercardPilia2.save()

        try:
            mastercardPiliaErrata.save()
        except IntegrityError:
            pass
        try:
            with transaction.atomic():
                Transazione(data=datetime(2018, 6, 14, 15, 30, 00), costo=5.02, biglietto=dodiciCorse, utente=user, cartaDiCredito=mastercardPilia).save()
        except IntegrityError:
            pass

    def testFindModels(self):
        self.assertEqual(len(Biglietto.objects.all()), 1)
        self.assertEqual(len(CartaDiCredito.objects.all()), 2)
        self.assertEqual(len(Transazione.objects.all()), 1)
        #self.assertEqual(len(user.object.all()), 3)