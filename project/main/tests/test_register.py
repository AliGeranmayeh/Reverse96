from .test_setUp import Test_SetUp

class TestRegister(Test_SetUp):
    def test_user_cannot_register_with_no_data(self):
        #register_url= "api/register/"
        response = self.client.post(self.regiater_url)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 400)