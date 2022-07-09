from .test_setUp import Test_SetUp
from django.contrib.auth import get_user_model
from faker import Faker
from random import randint

class TestSearch(Test_SetUp):
    def test_search_cant_show_unmatching_query(self):
        test_search = 'sdas'
        search_url= f"api/search/{test_search}"
        response = self.client.get(search_url, format="json")
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 302)