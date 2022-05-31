from datetime import timedelta
from random import randint
from unittest import mock

from faker import Faker
from rest_framework_simplejwt.utils import aware_utcnow

from .test_setUp import Test_SetUp
from django.contrib.auth import get_user_model
from functools import partial
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import CustomUser as User


class TestLogOut(Test_SetUp):
    login_url = reverse('login')
    refresh_token_url = reverse('refresh-token')
    logout_url = reverse('logout')

    email = 'test@user.com'
    password = 'kah2ie3urh4k'

    def setUp(self):
        self.fake = Faker()
        self.user_data = {
            "username": self.fake.email().split('@')[0],
            "email": self.fake.email(),
            "password": "12345",
            "address": self.fake.address(),
            "name": self.fake.name(),
            "phone_number": f'{randint(1000000000, 9999999999)}',
            "is_active": True
        }
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=True
        )

    def _login(self):
        data = {
            "username": self.user_data['username'],
            "password": self.user_data['password'],
        }
        r = self.client.post(self.login_url, data)
        body = r.json()
        if 'access' in body:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer %s' % body['access'])
        return r.status_code, body

    def test_logout_response_200(self):
        _, body = self._login()
        data = {'refresh': body['refresh']}
        r = self.client.post(self.logout_url, data)
        body = r.content
        #import pdb; pdb.set_trace()
        self.assertEquals(r.status_code, 204, body)

        self.assertFalse(body, body)

    def test_logout_with_bad_refresh_token_response_400(self):
        self._login()
        data = {'refresh': 'dsf.sdfsdf.sdf'}
        r = self.client.post(self.logout_url, data)
        body = r.json()
        self.assertEquals(r.status_code, 400, body)
        self.assertTrue(body, body)

    def test_logout_refresh_token_in_blacklist(self):
        _, body = self._login()
        #import pdb; pdb.set_trace()
        r = self.client.post(self.logout_url, body)
        token = partial(RefreshToken, body['refresh'])
        self.assertRaises(TokenError, token)

    