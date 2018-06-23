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
        dodici_corse = Biglietto(nome="Dodici Corse", validitaGiorni=12, costo=13.10, tipologia='3')
        annuale = Biglietto(nome="Abbonamento Annuale", validitaGiorni=365, costo=200.00, tipologia='5')
        mensile_studenti = Biglietto(nome="Abbonamento Mensile Studenti", validitaGiorni=30, costo=21.00, tipologia='1')
        singolo = Biglietto(nome="Corsa Singola", validitaGiorni=1, costo=1.30, tipologia='2')

        #Salvataggio biglietti
        dodici_corse.save()
        annuale.save()
        mensile_studenti.save()
        singolo.save()

        self.obj_count = Biglietto.objects.all().count()
        self.dodici = dodici_corse

    #Controllo di correttezza del numero di biglietti creati
    def test_ticket_count(self):
        self.assertEqual(self.obj_count, 4)

    #Controllo di correttezza del numero di biglietti creati (errato)
    def test_ticket_count_wrong(self):
        self.assertNotEqual(self.obj_count, 5)

    #Controllo sulla correttezza del nome del biglietto
    def test_ticket_name(self):
        self.assertEqual(self.dodici.get_full_name(), "Dodici Corse (Tipo: Biglietto 12 Corse, Validita: 12 giorni) Prezzo: 13.10 €")


#Test sulla creazione delle carte di credito
class CartaDiCreditoTest(TransactionTestCase):

    def setUp(self):
        self.c = Client()

        user_data = {'username': 'studente', 'password1': '12345678pw', 'password2': '12345678pw'}
        self.client.post('/signup/', user_data)

        login_data = {'username': 'studente', 'password': '12345678pw'}
        self.response = self.client.post('/login/', login_data, follow=True)
        self.user = self.response.context['user']

        #Creazione carte di credito corrette
        mastercard_pilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=2021, cvv='123', user=self.user)
        mastercard_pilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2022, cvv='321', user=self.user)

        #Creazione carta di credito errata (viola vincolo unique)
        mastercard_pilia_errata = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2015, cvv='421', user=self.user)

        #Salvataggio carte
        mastercard_pilia.save()
        mastercard_pilia2.save()

        #Test sull'aggiunta della carta errata
        try:
            mastercard_pilia_errata.save()
        except IntegrityError:
            pass
        self.obj_num = CartaDiCredito.objects.all().count()
        self.card1 = mastercard_pilia
        self.card2 = mastercard_pilia2

    #Test sul numero delle carte di credito
    def test_card_number(self):
        self.assertEqual(len(CartaDiCredito.objects.all()), 2)

    def test_card_number_wrong(self):
        self.assertNotEqual(self.obj_num, 3)

    def test_unit_card_get_name(self):
        self.assertEqual(self.card1.get_full_name(), "Carta di Credito 0123456789012345 (Scadenza: 1/2021)")
