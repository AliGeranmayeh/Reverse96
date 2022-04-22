from .test_setUp import Test_SetUp
from django.contrib.auth import get_user_model
from faker import Faker

class TestLogin(Test_SetUp):
    def test_user_cannot_login_without_email_verification(self):
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=False
        )
        data = {
            "username": self.user_data['username'],
            "password":self.user_data['password'],
        }
        res = self.client.post(self.login_url,data,format='json')
        #import pdb; pdb.set_trace()
        self.assertEqual(res.status_code, 403)

    def test_username_doesnot_exist(self):
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=False
        )
        fake = Faker()
        data={
            "username": fake.email().split("@")[0],
            "password":self.user_data['password']
        }
        res = self.client.post(self.login_url,data,format='json')
        self.assertEqual(res.status_code,404)

    def test_email_doesnot_exist(self):
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=False
        )
        fake = Faker()
        data={
            "username":fake.email(),
            "password":self.user_data['password']
        }
        res = self.client.post(self.login_url,data,format='json')
        self.assertEqual(res.status_code,404)