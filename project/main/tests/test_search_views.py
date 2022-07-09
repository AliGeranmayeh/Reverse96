from .test_setUp import Test_SetUp
from django.contrib.auth import get_user_model
from faker import Faker
from random import randint

class TestSearch(Test_SetUp):
    def test_search_cant_show_unmatching_query(self):
        pass