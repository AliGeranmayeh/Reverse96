from .test_setUp import Test_SetUp


class TestPublicProfileView(Test_SetUp):

    def test_user_cannot_see_public_profile(self):
        url = "/api/public-profile/zlkg-p"
        res = self.client.get(url, format="json")
        self.assertEqual(res.status_code, 404)
    
        