from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_create_user_successful(self):
        username = "lkksgfkjr"
        password = "12345"
        phone_number = 3045439051111
        address = "tehran"
        email = "etjenfa@hi2.in"
        name = "ali"
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            phone_number=phone_number,
            address=address,
            email=email,
            name=name
        )
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.email, email)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.address, address)
        self.assertEqual(user.name, name)