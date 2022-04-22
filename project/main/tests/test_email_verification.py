from .test_setUp import Test_SetUp
from django.contrib.auth import get_user_model
from user.models import EmailValidation
from faker import Faker

class TestEmailVerification(Test_SetUp):
    def test_user_cannot_verify_without_correct_code(self):
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=False
        )
        email_verification = EmailValidation.objects.create(email=self.user_data['email'],code=1234)
        data = {
            "email": self.user_data['email'],
            "code":4326
        }
        
        res = self.client.post(self.email_verification_url,data,format='json')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'],"wrong code")


    def test_user_can_verify_with_correct_code_and_email(self):
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=False
        )
        email_verification = EmailValidation.objects.create(email=self.user_data['email'],code=1234)
        data = {
            "email": self.user_data['email'],
            "code":1234
        }
        
        res = self.client.post(self.email_verification_url,data,format='json')
        self.assertEqual(res.status_code, 200)

    
    def test_user_cannot_verify_email_with_wrong_email_and_existing_code(self):
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=False
        )
        email_verification = EmailValidation.objects.create(email=self.user_data['email'],code=1234)
        fake=Faker()
        data = {
            "email": fake.email(),
            "code":1234
        }
        res = self.client.post(self.email_verification_url,data,format='json')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'],"Invalid credentials")


    def test_user_cannot_verify_email_twice(self):
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=True
        )
        email_verification = EmailValidation.objects.create(email=self.user_data['email'],code=1234)
        fake=Faker()
        data = {
            "email":self.user_data['email'],
            "code":1234
        }
        res = self.client.post(self.email_verification_url,data,format='json')
        self.assertEqual(res.status_code, 208)
