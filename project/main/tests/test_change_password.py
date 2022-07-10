from .test_setUp import Test_SetUp
from django.contrib.auth import get_user_model


class TestPublicProfileView(Test_SetUp):

    def test_user_can_change_password_correctly(self):
        pass