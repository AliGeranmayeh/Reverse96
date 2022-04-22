from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from random import randint

class Test_SetUp(APITestCase):
    

    def setUp(self):
        self.fake = Faker()
        self.regiater_url= reverse('register')

        self.user_data = {
            "username": "ali" ,
            "email": self.fake.email(),
            "password": "12345",
            "address": self.fake.address(),
            "name": self.fake.name(),
            "phone_number": randint(1000000000, 9999999999),
            "is_active":"True"
        }

        return super().setUp()


    def tearDown(self):
        return super().tearDown()