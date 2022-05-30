from .test_setUp import Test_SetUp


# class TestPublicProfileView(Test_SetUp):
#
#     def test_user_cannot_see_public_profile(self):
#         url = "/api/public-profile/zlkg-p"
#         res = self.client.get(url, format="json")
#         self.assertEqual(res.status_code, 404)
#
#     def test_user_can_see_public_profile(self):
#         register_url="/api/register"
#         self.client.post(register_url,self.user_data,format="json")
#         public_profile_url = f"/api/public-profile/{self.user_data['username']}"
#         res = self.client.get(public_profile_url, format="json")
#         #import pdb; pdb.set_trace()
#         self.assertEqual(res.status_code, 200)
    
        