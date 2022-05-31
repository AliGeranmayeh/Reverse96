from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from random import randint

class Test_SetUp(APITestCase):
    

    def setUp(self):
        self.fake = Faker()
        self.register_url= reverse('register')
        self.category_url = reverse('limited-area-category')
        self.login_url= reverse('login')
        self.email_verification_url= reverse('email-activision')
        self.user_data = {
            "username": self.fake.email().split('@')[0],
            "email": self.fake.email(),
            "password": "12345",
            "address": self.fake.address(),
            "name": self.fake.name(),
            "phone_number": f'{randint(1000000000, 9999999999)}',
            "is_active":True
        }
        self.user_data2 = {
            "username": self.fake.email().split('@')[0],
            "email": self.fake.email(),
            "password": "12345",
            "address": self.fake.address(),
            "name": self.fake.name(),
            "phone_number": f'{randint(1000000000, 9999999999)}',
            "is_active": True
        }
        self.location_data = {
            "name": "Azadi",
            "long": 2,
            "latt": 5,
            "place_category": "3"
        }

        self.location_data1 = {
            "name": "nazi abad",
            "long": 1,
            "latt": 3,
            "place_category": "1"
        }
        self.location_data2 = {
            "name": "zaferanie",
            "long": 3,
            "latt": 4,
            "place_category": "1"
        }


        return super().setUp()


    def tearDown(self):
        return super().tearDown()