from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from main.forms import LoginForm, RegistrationForm
import unittest

User = get_user_model()


class Registrarion_and_authorization_Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_registation_200(self):
        avatar = SimpleUploadedFile('foto.jpg', content=b'', content_type='image/jpg')
        response = self.client.post(
            '/registration/',
            {'username': 'testuser',
             'password': '12345Qwert',
             'confirm_password': '12345Qwert',
             'email': 'wadwd@gmail.com',
             'first_name': 'First',
             'last_name': 'User',
             'avatar': avatar}
        )
        self.assertEqual(response.status_code, 200)

    def test_authorization_200(self):
        response = self.client.post(
            '/login/',
            {'username': 'testuser',
             'password': '12345Qwert'}
        )
        self.assertEqual(response.status_code, 200)


class TestForm(unittest.TestCase):
    def test_login_in_valid(self):
        request_form = LoginForm()
        self.assertFalse(request_form.is_valid())

    def test_registaration_in_valid(self):
        request_form = RegistrationForm()
        self.assertFalse(request_form.is_valid())
