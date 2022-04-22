from .test_setUp import Test_SetUp
from django.contrib.auth import get_user_model

class TestRegister(Test_SetUp):
    def test_user_cannot_register_with_no_data(self):
        #register_url= "api/register/"
        response = self.client.post(self.regiater_url)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 400)

    def test_user_can_register_correctly(self):
        res= self.client.post(self.regiater_url,self.user_data,format='json')
        #import pdb; pdb.set_trace()
        self.assertEqual(res.data['message']['username'], self.user_data['username'])
        self.assertEqual(res.data['message']['email'], self.user_data['email'])
        self.assertEqual(res.data['message']['phone_number'], self.user_data['phone_number'])
        self.assertEqual(res.data['message']['address'], self.user_data['address'])
        self.assertEqual(res.data['message']['name'], self.user_data['name'])
        self.assertEqual(res.data['message']['is_active'], self.user_data['is_active'])
        self.assertEqual(res.status_code,201)

    def test_user_cannot_register_twice(self):
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=self.user_data['is_active']
        )
        res= self.client.post(self.regiater_url,self.user_data,format='json')
        self.assertEqual(res.status_code,400)