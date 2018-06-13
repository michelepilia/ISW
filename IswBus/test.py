
import unittest

from django.contrib.auth import authenticate
from django.test import TestCase, Client
from IswBus.models import *
from datetime import datetime

class ModelTest(TestCase):
    def setUp(self):
        self.user = User(username="admin", email="email@email.com", password="administrator")

        dodiciCorse = Biglietto(nome='dodiciCorse', validitaGiorni=10, costo=2.00, tipologia='3')
        dodiciCorse.save()

        mastercardPilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=21, cvv='123')
        mastercardPilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=22, cvv='321')
        #mastercardPiliaErrata = CartaDiCredito(numero='54321098765432109', mese_scadenza=02, anno_scadenza=22, cvv='321')
        mastercardPilia.save()
        mastercardPilia2.save()
        # mastercardPiliaErrata.save()

        acquisto01 = Transazione(data= datetime.datetime(2018, 6, 14, 15 ,30 , 00), costo=05.02, tipo_biglietto= '3')
        acquisto01.save()

    def testFindModels(self):
        self.assertEqual(len(Biglietto.object.all()), 1)
        self.assertEqual(len(CartaDiCredito.object.all()), 2)
        self.assertEqual(len(Transazione.object.all()), 1)

        #signPilia = Utente(username='SignorPilia', password='passauord' )