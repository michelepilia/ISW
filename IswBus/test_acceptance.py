from IswBus.models import *
from django.test import TestCase, Client
from IswBus.models import CartaDiCredito, Biglietto, Transazione


# Test sul funzionamento del login
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

        mastercard_pilia.save()
        mastercard_pilia2.save()
    
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

    # Test sulla corretta visualizzazione delle possibili operazioni durante l'acquisto di un biglietto
    def test_ticket_view(self):
        self.response = self.c.post('/ticket/%d/' % self.ticket1.id)
        self.assertContains(self.response, 'Acquista Biglietto')
        self.assertContains(self.response, 'Carta di Credito 0123456789012345')
        self.assertContains(self.response, 'Carta di Credito 5432109876543210')
        self.assertContains(self.response, 'Acquista')
        self.assertContains(self.response, 'Aggiungi Carta')

    '''
    Test sulla visualizzazione delle possibili operazioni durante l'acquisto di un biglietto, quando non si possiede di
    una carta di credito registrata
    '''
    def test_ticket_view_user_without_card(self):
        self.c.post('/logout/')
        self.c.post('/login/', self.login2_data, follow=True)
        self.response = self.c.post('/ticket/%d/' % self.ticket1.id)
        self.assertContains(self.response, 'Acquista Biglietto')
        self.assertNotContains(self.response, 'Carta di Credito')
        self.assertContains(self.response, 'Aggiungi Carta')

# Test sulla vista delle statistiche dell'ultimo mese
class TestVisualizzaStatistiche(TestCase):
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
        mastercard_pilia = CartaDiCredito(numero='0123456789012345', mese_scadenza=1, anno_scadenza=2021, cvv='123',
                                         user=self.user)
        mastercard_pilia2 = CartaDiCredito(numero='5432109876543210', mese_scadenza=2, anno_scadenza=2022, cvv='321',
                                          user=self.user)

        # Dati Biglietti
        dodiciCorse = Biglietto(nome="Dodici Corse", validitaGiorni=12, costo=13.10, tipologia='3')
        annuale = Biglietto(nome="Abbonamento Annuale", validitaGiorni=365, costo=200.00, tipologia='5')
        mensile = Biglietto(nome="Abbonamento Mensile", validitaGiorni=30, costo=30.00, tipologia='1')
        mensile_studenti = Biglietto(nome="Abbonamento Mensile Studenti", validitaGiorni=30, costo=26.00, tipologia='1')

        mastercard_pilia.save()
        mastercard_pilia2.save()

        dodiciCorse.save()
        annuale.save()
        mensile_studenti.save()
        mensile.save()

        transazione1 = Transazione(data=timezone.now() + timezone.timedelta(days=-26),
                                   costo=dodiciCorse.costo,
                                   biglietto=dodiciCorse,
                                   utente=self.user,
                                   cartaDiCredito=mastercard_pilia2)
        transazione2 = Transazione(data=timezone.now() + timezone.timedelta(days=-10),
                                   costo=annuale.costo,
                                   biglietto=annuale,
                                   utente=self.user,
                                   cartaDiCredito=mastercard_pilia2)
        transazione3 = Transazione(data=timezone.now() + timezone.timedelta(days=-4),
                                   costo=mensile.costo,
                                   biglietto=mensile,
                                   utente=self.user,
                                   cartaDiCredito=mastercard_pilia2)
        transazione4 = Transazione(data=timezone.now() + timezone.timedelta(days=-17),
                                   costo=mensile.costo,
                                   biglietto=mensile,
                                   utente=self.user,
                                   cartaDiCredito=mastercard_pilia)
        transazione5 = Transazione(data=timezone.now() + timezone.timedelta(days=-45),
                                   costo=mensile_studenti.costo,
                                   biglietto=mensile_studenti,
                                   utente=self.user,
                                   cartaDiCredito=mastercard_pilia)
        transazione6 = Transazione(data=timezone.now() + timezone.timedelta(days=-50),
                                   costo=dodiciCorse.costo,
                                   biglietto=dodiciCorse,
                                   utente=self.user,
                                   cartaDiCredito=mastercard_pilia)

        transazione1.save()
        transazione2.save()
        transazione3.save()
        transazione4.save()
        transazione5.save()
        transazione6.save()

        self.transazione1 = transazione1
        self.transazione2 = transazione2
        self.transazione3 = transazione3
        self.transazione4 = transazione4
        self.transazione5 = transazione5
        self.transazione6 = transazione6

        self.dodici = dodiciCorse
        self.annuale = annuale
        self.mensile = mensile
        self.mensile_studenti = mensile_studenti

    # Test sulla vista delle statistiche dell'ultimo mese (biglietti acquistati, spesa totale e biglietto più acquistato)
    def test_view_statistics(self):
        self.response = self.c.post('/statistics/')
        self.assertContains(self.response, 'Statistiche ultimo mese')
        self.assertContains(self.response, 'Numero biglietti acquistati: 4')
        self.assertContains(self.response, 'Spesa effettuata: 273.10')
        self.assertContains(self.response, 'Biglietto più acquistato: Abbonamento Mensile')
        self.assertNotContains(self.response, 'Numero biglietti acquistati: 6')