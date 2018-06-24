from django.test import TestCase, Client


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
