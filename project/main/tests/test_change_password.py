from .test_setUp import Test_SetUp
from django.contrib.auth import get_user_model


class TestPublicProfileView(Test_SetUp):

    def test_user_can_change_password_correctly(self):
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=True
        )

        login_data = {
            "username": self.user_data['username'],
            "password": self.user_data['password'],
        }

        res = self.client.post(self.login_url, login_data, format='json')

        new_password = {
            'password': "@123ads98"
        }
        data = {
            "old_password":self.user_data['password'],
            'password': new_password['password'],
            'password2': new_password['password']

        }
        header = self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % res.json()['access'])
        response = self.client.patch(self.change_password_url, data, format='json')
        #import pdb; pdb.set_trace()

        self.assertEqual(response.status_code, 205)

        login_data2= {
            "username": self.user_data["username"],
            "password": new_password["password"]
        }
        login_res2 = self.client.post(self.login_url, login_data2, format='json')
        self.assertEqual(login_res2.status_code, 200)
        fail_login_res = self.client.post(self.login_url, login_data, format='json')
        #import pdb; pdb.set_trace()
        self.assertEqual(fail_login_res.status_code,404)
        self.assertEqual(fail_login_res.data["message"],'wrong password')


