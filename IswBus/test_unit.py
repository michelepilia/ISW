'''
ISW Bus Ticket
ISW-Gruppo-4-65215-65237-65205-65195
65215 - Michele Pilia
65237 - Massimo Zara
65205 - Andrea Marotto
65195 - Giulio Sprega
'''

import pytz
from django.test import Client, TransactionTestCase, TestCase, RequestFactory
from IswBus.models import *
from IswBus.forms import *
from django.db import IntegrityError


# Test sulla creazione dei biglietti
class BigliettoTest(TransactionTestCase):

    def setUp(self):

        # Creazione biglietti
        dodici_corse = Biglietto(nome="Dodici Corse", validitaGiorni=12, costo=13.10, tipologia='3')
        annuale = Biglietto(nome="Abbonamento Annuale", validitaGiorni=365, costo=200.00, tipologia='5')
        mensile_studenti = Biglietto(nome="Abbonamento Mensile Studenti", validitaGiorni=30, costo=21.00, tipologia='1')
        singolo = Biglietto(nome="Corsa Singola", validitaGiorni=1, costo=1.30, tipologia='2')
        integrato = Biglietto(nome="Corsa Singola Integrata 120 minuti", validitaGiorni=1, costo=2.00, tipologia='4')
        mensile = Biglietto(nome="Abbonamento Mensile", validitaGiorni=30, costo=30.00, tipologia='1')
        mensile_pensionati = Biglietto(nome="Abbonamento Mensile Pensionati", validitaGiorni=30, costo=25.00, tipologia='1')

        # Salvataggio biglietti
        dodici_corse.save()
        annuale.save()
        mensile_studenti.save()
        singolo.save()
        integrato.save()
        mensile.save()
        mensile_pensionati.save()

        self.obj_count = Biglietto.objects.all().count()
        self.dodici = dodici_corse
        self.mensile = mensile

    # Controllo di correttezza del numero di biglietti creati
    def test_ticket_count(self):
        self.assertEqual(self.obj_count, 7)

    # Controllo di correttezza del numero di biglietti creati (errato)
    def test_ticket_count_wrong(self):
        self.assertNotEqual(self.obj_count, 6)

    # Controllo di correttezza del numero di biglietti creati (errato) 2
    def test_ticket_count_wrong_2(self):
        self.assertNotEqual(self.obj_count, 8)

    # Controllo sulla correttezza del nome del biglietto
    def test_ticket_name(self):
        self.assertEqual(self.dodici.get_full_name(), "Dodici Corse (Tipo: Biglietto 12 Corse, Validita: 12 giorni) Prezzo: 13.10 €")

    # Controllo sulla correttezza del nome del biglietto 2
    def test_ticket_name_2(self):
        self.assertEqual(self.mensile.get_full_name(), "Abbonamento Mensile (Tipo: Abbonamento Mensile, Validita: 30 giorni) Prezzo: 30.00 €")

    # Controllo sulla correttezza del nome del biglietto (errato)
    def test_ticket_name_wrong(self):
        self.assertNotEqual(str(self.mensile), "Abbonamento Mensile (Tipo: Abbonamento Mensile, Validita: 20 giorni) Prezzo: 15.00 €")


# Test sulla creazione delle carte di credito
class CartaDiCreditoTest(TransactionTestCase):

    def setUp(self):
        self.c = Client()

        user_data = {'username': 'studente', 'password1': '12345678pw', 'password2': '12345678pw'}
        self.client.post('/signup/', user_data)

        login_data = {'username': 'studente', 'password': '12345678pw'}
        self.response = self.client.post('/login/', login_data, follow=True)
        self.user = self.response.context['user']

        # Creazione carte di credito corrette
        mastercard_pilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=2021, cvv='123', user=self.user)
        mastercard_pilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2022, cvv='321', user=self.user)

        # Creazione carta di credito errata (viola vincolo unique)
        mastercard_pilia_errata = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2015, cvv='421', user=self.user)

        # Salvataggio carte
        mastercard_pilia.save()
        mastercard_pilia2.save()

        # Test sull'aggiunta della carta errata
        try:
            mastercard_pilia_errata.save()
        except IntegrityError:
            pass
        self.obj_num = CartaDiCredito.objects.all().count()
        self.card1 = mastercard_pilia
        self.card2 = mastercard_pilia2

    # Test sul numero delle carte di credito
    def test_card_number(self):
        self.assertEqual(len(CartaDiCredito.objects.all()), 2)

    # Test sul numero delle carte di credito (errato)
    def test_card_number_wrong(self):
        self.assertNotEqual(self.obj_num, 3)

    # Test sul numero delle carte di credito (errato) 2
    def test_unit_card_num_wrong2(self):
        self.assertNotEqual(self.obj_num, 1)

    # Test sul nome delle carte di credito
    def test_unit_card_get_name(self):
        self.assertEqual(self.card1.get_full_name(), "Carta di Credito 0123456789012345 (Scadenza: 1/2021)")

    # Test sul nome delle carte di credito 2
    def test_unit_card_get_name2(self):
        self.assertEqual(self.card2.get_full_name(), "Carta di Credito 5432109876543210 (Scadenza: 2/2022)")

    # Test sul nome delle carte di credito (errato)
    def test_unit_card_get_name_wrong(self):
        self.assertNotEqual(self.card2.get_full_name(), "Carta di Credito 1111222233334444 (Scadenza: 11/2021)")


# Test sul corretto funzionamento del form della carta di credito
class CreditCardFormTest(TestCase):
    # Controllo sull'inserimento di un numero di carta vuoto
    def test_card_form_empty_number(self):
        dati = {'card_number': '',
                'expiration_month': '11',
                'expiration_year': '2021',
                'cvv': '123'}
        form = CreditCardForm(dati)
        self.assertFalse(form.is_valid())

    # Controllo sul corretto inserimento di un mese di scadenza
    def test_card_form_empty_month(self):
        dati = {'card_number': '1111222233334444',
                'expiration_month': '',
                'expiration_year': '2021',
                'cvv': '123'}
        form = CreditCardForm(dati)
        self.assertFalse(form.is_valid())

    # Controllo sul corretto inserimento di un anno di scadenza
    def test_card_form_empty_year(self):
        dati = {'card_number': '1111222233334444',
                'expiration_month': '11',
                'expiration_year': '',
                'cvv': '123'}
        form = CreditCardForm(dati)
        self.assertFalse(form.is_valid())

    # Controllo sul corretto inserimento del CVV
    def test_card_form_empty_cvv(self):
        dati = {'card_number': '1111222233334444',
                'expiration_month': '11',
                'expiration_year': '2021',
                'cvv': ''}
        form = CreditCardForm(dati)
        self.assertFalse(form.is_valid())

    # Si controlla che la lunghezza del numero della carta non superi le 16 cifre
    def test_card_form_longer_number(self):
        dati = {'card_number': '111122223333444455',  # 18 cifre
                'expiration_month': '11',
                'expiration_year': '2021',
                'cvv': '123'}
        form = CreditCardForm(dati)
        self.assertFalse(form.is_valid())

    # Si controlla che il numero equivalente al mese inserito non sia maggiore di 12
    def test_card_form_higher_month(self):
        dati = {'card_number': '1111222233334444',
                'expiration_month': '13',
                'expiration_year': '2021',
                'cvv': '123'}
        form = CreditCardForm(dati)
        self.assertFalse(form.is_valid())

    # Si controlla che il numero equivalente al mese inserito non sia minore di 1
    def test_card_form_lower_month(self):
        dati = {'card_number': '1111222233334444',
                'expiration_month': '-1',
                'expiration_year': '2021',
                'cvv': '123'}
        form = CreditCardForm(dati)
        self.assertFalse(form.is_valid())

    # Controllo sulla correttezza dell'anno inserito
    def test_card_form_lower_year(self):
        dati = {'card_number': '1111222233334444',
                'expiration_month': '12',
                'expiration_year': '2008',
                'cvv': '123'}
        form = CreditCardForm(dati)
        self.assertFalse(form.is_valid())

    # Controllo sulla lunghezza del CVV
    def test_card_form_longer_cvv(self):
        dati = {'card_number': '1111222233334444',
                'expiration_month': '11',
                'expiration_year': '2021',
                'cvv': '12345'}
        form = CreditCardForm(dati)
        self.assertFalse(form.is_valid())

    # Test sul corretto funzionamento dei form, si inseriscono solo dati validi
    def test_card_ok(self):
        dati = {'card_number': '1111222233334444',
                'expiration_month': '11',
                'expiration_year': '2020',
                'cvv': '123'}
        form = CreditCardForm(dati)
        self.assertTrue(form.is_valid())


# Test per il controllo del corretto funzionamento delle transazioni
class TransazioneTest(TransactionTestCase):
    def setUp(self):
        self.c = Client()

        # Dati Utente
        user_data = {'username': 'studente',
                        'password1': '12345678pw',
                        'password2': '12345678pw'}
        self.client.post('/signup/', user_data)


        login_data = {'username': 'studente', 'password': '12345678pw'}
        self.response= self.client.post('/login/', login_data, follow=True)
        self.user = self.response.context['user']

        # Dati Carte
        mastercard_pilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=2021, cvv='123',
                                         user=self.user)
        mastercard_pilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2022, cvv='321',
                                          user=self.user)

        mastercard_pilia.save()
        mastercard_pilia2.save()

        #Dati Biglietti
        dodiciCorse = Biglietto(nome="Dodici Corse", validitaGiorni=12, costo=13.10, tipologia='3')
        annuale = Biglietto(nome="Abbonamento Annuale", validitaGiorni=365, costo=200.00, tipologia='5')

        dodiciCorse.save()
        annuale.save()

        transazione1 = Transazione(data=datetime(2017, 12, 6, 16, 29, 43, tzinfo=pytz.UTC),
                                   costo=dodiciCorse.costo,
                                   biglietto=dodiciCorse,
                                   utente=self.user,
                                   cartaDiCredito=mastercard_pilia)

        transazione2 = Transazione(data=datetime(2015, 7, 14, 12, 30, 43, tzinfo=pytz.UTC),
                                   costo=annuale.costo,
                                   biglietto=annuale,
                                   utente=self.user,
                                   cartaDiCredito=mastercard_pilia2)

        transazione1.save()
        transazione2.save()

        self.tr_one = transazione1
        self.tr_two = transazione2
        self.count = Transazione.objects.all().count()

    # Si verifica che le transazioni siano 2
    def test_unit_transaction_count(self):
        self.assertEqual(self.count, 2)

    # Si verifica che le transazioni non siano 3
    def test_unit_transaction_count_wrong(self):
        self.assertNotEqual(self.count, 3)

    # Si verifica che la transazione non sia una
    def test_unit_transaction_count_wrong2(self):
        self.assertNotEqual(self.count, 1)


