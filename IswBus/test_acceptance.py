from django.test import TestCase, Client


# Test sul funzionamento del login
from IswBus.models import CartaDiCredito


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
