
import unittest

from django.contrib.auth import authenticate
from django.test import TestCase, Client
from IswBus.models import *

class ModelTest(TestCase):
    def setUp(self):
        self.user = User(username="admin", email="email@email.com", password="administrator")

        dodiciCorse = Biglietto(nome='dodiciCorse', validitaGiorni=10, costo=2.00, tipologia='3')
        dodiciCorse.save()

    def testFindModels(self):
        self.assertEqual(len(Biglietto.object.all()), 1)

        mastercardPilia = CartaDiCredito(numero = '0123456789012345', mese_scadenza=01, anno_scadenza=21, cvv='123')
        mastercardPilia2 = CartaDiCredito(numero= '5432109876543210', mese_scadenza=02, anno_scadenza=22, cvv='321')
        #mastercardPiliaErrata = CartaDiCredito(numero='54321098765432109', mese_scadenza=02, anno_scadenza=22, cvv='321')
        mastercardPilia.save()
        mastercardPilia2.save()
        #mastercardPiliaErrata.save()

    def testFindModels(self):
        self.assertEqual(len(CartaDiCredito.object.all()), 2)

        #signPilia = Utente(username='SignorPilia', password='passauord' )