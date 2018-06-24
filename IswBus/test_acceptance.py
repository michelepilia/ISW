from datetime import datetime

import pytz
from django.test import TestCase, Client

# Test sul funzionamento del login
from IswBus.models import CartaDiCredito, Biglietto, Transazione


class TestLogin(TestCase):
    def setUp(self):
        self.c = Client()

        user_data = {'username': 'studente',
                     'password1': '12345678pw',
                     'password2': '12345678pw'}
        self.client.post('/signup/', user_data)

    # Test sul login corretto
    def test_login_ok(self):
        self.login_data = {
            'username': 'studente',
            'password': '12345678pw'
        }
        response = self.c.post('/login/', self.login_data, follow=True)
        self.assertTrue(response.context['user'].is_active)

    # Test sul login con password sbagliata
    def test_login_wrong_pw(self):
        self.not_valid_data = {
            'username': 'studente',
            'password': 'sicuramentesbagliato'
        }
        response = self.c.post('/login/', self.not_valid_data, follow=True)
        self.assertFalse(response.context['user'].is_active)

    # Test sul login con username non registrato
    def test_login_utente_non_esiste(self):
        self.login_data = {
            'username': 'nonesisto',
            'password': 'miaomiao'
        }
        response = self.c.post('/login/', self.login_data, follow=True)
        self.assertFalse(response.context['user'].is_active)

    # Test sul login con password vuota
    def test_login_pw_non_esiste(self):
        self.login_data = {
            'username': 'studente',
            'password': ''
        }
        response = self.c.post('/login/', self.login_data, follow=True)
        self.assertFalse(response.context['user'].is_active)


# Test sul corretto funzionamento del logout
class TestLogout(TestCase):
    def setUp(self):
        self.c = Client()

        user_data = {'username': 'studente',
                     'password1': '12345678pw',
                     'password2': '12345678pw'}
        self.client.post('/signup/', user_data)

        login_data = {'username': 'studente', 'password': '12345678pw'}
        self.response = self.c.post('/login/', login_data, follow=True)
        self.user = self.response.context['user']

    def test_logout_success(self):
        self.assertContains(self.response, 'Logout')
        self.response = self.c.post('/logout/')
        self.assertEquals(self.response.url, 'login')


# Test sul funzionamento della registrazione
class TestRegistrazione(TestCase):
    def setUp(self):
        self.c = Client()

        user_data = {'username': 'studente',
                     'password1': '12345678pw',
                     'password2': '12345678pw'}
        self.client.post('/signup/', user_data)

        login_data = {'username': 'studente', 'password': '12345678pw'}
        self.response = self.c.post('/login/', login_data, follow=True)
        self.user = self.response.context['user']

    # Test sull'utente attivo (fallisci se non è attivo)
    def test_utente_attivo(self):
        self.failUnless(self.user.is_active)

    # Test sulla registrazione
    def test_registrazione_ok(self):
        signup_data = {'username': 'luigi',
                       'password1': 'rossirossi',
                       'password2': 'rossirossi'}
        self.response = self.client.post('/signup/', signup_data)
        self.assertEqual(self.response.url, '/tickets/')

    # Test sullo username già registrato
    def test_signup_username_exist(self):
        signup_data = {'username': 'studente',
                       'password1': 'rossirossi',
                       'password2': 'rossirossi'}
        self.response = self.client.post('/signup/', signup_data)
        self.assertContains(self.response, 'A user with that username already exists.')

    # Test sullo username non valido
    def test_signup_username_not_valid(self):
        signup_data = {'username': 'lui/*gi',
                       'password1': 'rossirossi',
                       'password2': 'rossirossi'}
        self.response = self.client.post('/signup/', signup_data)
        self.assertContains(self.response, 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.')

    # Test sulla password non ammessa (troppo semplice)
    def test_signup_pw_too_common(self):
        signup_data = {'username': 'studente12',
                       'password1': '12345678',
                       'password2': '12345678'}
        self.response = self.client.post('/signup/', signup_data)
        self.assertContains(self.response, 'This password is too common.')


# Test sul corretto inserimento della carta di credito
class TestInserireCarta(TestCase):
    def setUp(self):
        self.c = Client()

        user_data = {'username': 'studente',
                     'password1': '12345678pw',
                     'password2': '12345678pw'}
        self.c.post('/signup/', user_data)

        login_data = {'username': 'studente', 'password': '12345678pw'}
        self.response = self.c.post('/login/', login_data, follow=True)
        self.user = self.response.context['user']

        mastercard_pilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=2021, cvv='123', user=self.user)
        mastercard_pilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2022, cvv='321', user=self.user)

        mastercard_pilia.save()
        mastercard_pilia2.save()

        self.obj_num = CartaDiCredito.objects.all().count()
        self.card1 = mastercard_pilia
        self.card2 = mastercard_pilia2

    # Test sulla visualizzazione (deve mostrare una delle carte salvate, piu il bottone aggiungi carta)
    def test_initial_view(self):
        self.response = self.c.post('/cards/')
        self.assertContains(self.response, '0123456789012345')
        self.assertContains(self.response, 'Aggiungi Carta')

    # Test sul bottone (deve rimandare ad aggiungi carta)
    def test_aggiungi_carta_link(self):
        self.response = self.c.post('/add_card/')
        self.assertContains(self.response, 'Aggiungi Carta di Credito')

    # Test sull'aggiunta di una carta già registrata
    def test_carta_esistente_view(self):
        dati_carta = {'card_number': '0123456789012345', 'expiration_month': 11, 'expiration_year': 2022, 'cvv': '123'}
        self.response = self.c.post('/add_card/', dati_carta)
        self.assertContains(self.response, 'Carta di credito già esistente')

    # Test sul corretto inserimento (controllo la risposta)
    def test_ok_redirect(self):
        dati_carta = {'card_number': '3333666655553333', 'expiration_month': 11, 'expiration_year': 2022, 'cvv': '123'}
        self.response = self.c.post('/add_card/', dati_carta, follow=True)
        self.assertContains(self.response, '3333666655553333')
        self.assertContains(self.response, 'Carte di Credito')


# Test sulla correttezza del modifica carta
class TestModificareCarta(TestCase):
    def setUp(self):
        self.c = Client()

        user_data = {'username': 'studente',
                     'password1': '12345678pw',
                     'password2': '12345678pw'}
        self.c.post('/signup/', user_data)

        login_data = {'username': 'studente', 'password': '12345678pw'}
        self.response = self.c.post('/login/', login_data, follow=True)
        self.user = self.response.context['user']

        mastercard_pilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=2021, cvv='123', user=self.user)
        mastercard_pilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2022, cvv='321', user=self.user)

        self.obj_num = CartaDiCredito.objects.all().count()
        self.card1 = mastercard_pilia
        self.card2 = mastercard_pilia2

    ''' 
    TO BE FIXED
    # Test sulla vista iniziale (deve mostrare il dettaglio della carta, piu il bottone "Salva")
    def test_initial_view(self):
        self.id = self.card1.id
        self.response = self.c.post('/edit-card/%d/' % self.id, follow=True)
        self.assertContains(self.response, 'Modifica Carta di Credito')
        self.assertContains(self.response, 'Numero Carta di Credito')
        self.assertContains(self.response, 'Salva')
        
    # Test sulla vista dopo una modifica
    def test_after_edit(self):
        self.id = self.card1.id
        self.dati_carta = {
            'card_number': '4444777722220000',
            'expiration_month': '12',
            'expiration_year': '2023',
            'cvv': '125'
        }
        self.response = self.c.post('/edit-card/%d/' % self.id, self.dati_carta, follow=True)
        self.assertContains(self.response, 'Carte di Credito')
        self.assertContains(self.response, '4444777722220000')
        self.assertNotContains(self.response, '0123456789012345')
    '''


class TestAcquistaBiglietto(TestCase):
    def setUp(self):
        self.c = Client()

        user1_data = {'username': 'studente',
                      'password1': '12345678pw',
                      'password2': '12345678pw'}

        user2_data = {'username': 'alunno',
                      'password1': '87654321pw',
                      'password2': '87654321pw'}
        self.c.post('/signup/', user1_data)
        self.c.post('/signup/', user2_data)

        login1_data = {'username': 'studente', 'password': '12345678pw'}
        self.login2_data = {'username': 'alunno', 'password': '87654321pw'}
        self.response1 = self.c.post('/login/', login1_data, follow=True)
        self.user1 = self.response1.context['user']

        mastercard_pilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=2021, cvv='123',
                                         user=self.user1)
        mastercard_pilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2022, cvv='321',
                                          user=self.user1)
        mastercard_pilia.save()
        mastercard_pilia2.save()

        biglietto1 = Biglietto(nome="Dodici Corse", validitaGiorni=12, costo=13.00, tipologia='3')
        biglietto2 = Biglietto(nome="Corsa Singola", validitaGiorni=1, costo=1.30, tipologia='1')

        biglietto1.save()
        biglietto2.save()

        self.obj_num = CartaDiCredito.objects.all().count()
        self.card1 = mastercard_pilia
        self.card2 = mastercard_pilia2
        self.ticket1 = biglietto1
        self.ticket2 = biglietto2

    # Si controlla la corretta visualizzazione dei due tipi di biglietti acquistabili
    def test_initial_view(self):
        self.response = self.c.post('/tickets/')
        self.assertContains(self.response, 'Dodici Corse')
        self.assertContains(self.response, 'Corsa Singola')


# Test correttezza viste transazioni
class TestVisualizzaTransazioni(TestCase):
    def setUp(self):
        self.c = Client()

        # Dati Utente
        user_data = {'username': 'studente',
                     'password1': '12345678pw',
                     'password2': '12345678pw'}
        self.c.post('/signup/', user_data)

        login_data = {'username': 'studente', 'password': '12345678pw'}
        self.response = self.c.post('/login/', login_data, follow=True)
        self.user = self.response.context['user']

        # Dati Carte
        mastercardPilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=2021, cvv='123', user=self.user)
        mastercardPilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2022, cvv='321', user=self.user)

        mastercardPilia.save()
        mastercardPilia2.save()

        # Dati Biglietti
        dodiciCorse = Biglietto(nome="Dodici Corse", validitaGiorni=12, costo=13.10, tipologia='3')
        annuale = Biglietto(nome="Abbonamento Annuale", validitaGiorni=365, costo=200.00, tipologia='5')

        dodiciCorse.save()
        annuale.save()

        transazione1 = Transazione(data=datetime(2017, 12, 6, 16, 29, 43, tzinfo=pytz.UTC),
                                   costo=dodiciCorse.costo,
                                   biglietto=dodiciCorse,
                                   utente=self.user,
                                   cartaDiCredito=mastercardPilia2)
        transazione2 = Transazione(data=datetime(2015, 7, 14, 12, 30, 43, tzinfo=pytz.UTC),
                                   costo=annuale.costo,
                                   biglietto=annuale,
                                   utente=self.user,
                                   cartaDiCredito=mastercardPilia)
        transazione1.save()
        transazione2.save()

        self.transazione1 = transazione1
        self.tr_one = transazione1
        self.tr_two = transazione2
        self.count = Transazione.objects.all().count()

    # Verifica viste biglietti acquistati
    def test_transazioni_view(self):
        self.response = self.c.post('/transactions/', follow=True)
        self.assertContains(self.response, 'Biglietti Acquistati')
        self.assertContains(self.response, 'Dodici Corse')
        self.assertContains(self.response, 'Abbonamento Annuale')

    # Verifica viste dettagli transazione
    def test_transazione_view(self):
        self.response = self.c.post('/transaction/%d' % self.transazione1.id, follow=True)
        self.assertContains(self.response, 'Dettaglio Transazione')
        self.assertContains(self.response, 'Giorni di validita: 12')
        self.assertContains(self.response, 'Dati Transazione')
        self.assertContains(self.response, 'Carta: Carta di Credito 5432109876543210')
