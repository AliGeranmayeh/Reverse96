from .test_setUp import Test_SetUp
from django.contrib.auth import get_user_model
from faker import Faker
from random import randint
from review.models import locations,review

class TestSearch(Test_SetUp):
    def test_search_cant_show_unmatching_query(self):
        test_search = 'sdas'
        search_url= f"/api/search/{test_search}"
        response = self.client.get(search_url, format="json")
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 404)

    def test_review_search_cant_show_unmatching_query(self):
        test_search = 'sdas'
        search_url= f"/api/r_search/{test_search}"
        response = self.client.get(search_url, format="json")
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 404)

    def test_user_search_cant_show_unmatching_query(self):
        test_search = 'sdas'
        search_url= f"/api/u_search/{test_search}"
        response = self.client.get(search_url, format="json")
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 404)

    def test_location_search_cant_show_unmatching_query(self):
        test_search = 'sdas'
        search_url= f"/api/l_search/{test_search}"
        response = self.client.get(search_url, format="json")
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 404)


    def test_location_search_show_matched_query(self):
        location = locations.objects.create(
            name=self.location_data["name"],
            long=self.location_data["long"],
            latt=self.location_data["latt"],
            place_category=self.location_data["place_category"]
        )
        location1 = locations.objects.create(
            name=self.location_data1["name"],
            long=self.location_data1["long"],
            latt=self.location_data1["latt"],
            place_category=self.location_data1["place_category"]
        )

        location2 = locations.objects.create(
            name=self.location_data2["name"],
            long=self.location_data2["long"],
            latt=self.location_data2["latt"],
            place_category=self.location_data2["place_category"]
        )
        test_search = 'az'
        search_url = f"/api/l_search/{test_search}"
        response = self.client.get(search_url, format="json")
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 302)
        name = list(response.data[0].items())[1][1]
        long = list(response.data[0].items())[3][1]
        latt = list(response.data[0].items())[4][1]
        self.assertEqual(name, f'{self.location_data["name"]}')
        self.assertEqual(long, f'{self.location_data["long"]}.000000000000000')
        self.assertEqual(latt, f'{self.location_data["latt"]}.000000000000000')

    def test_user_search_show_matched_query(self):
        user = get_user_model().objects.create_user(
            username="mohsen",
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=self.user_data['is_active']
        )

        user = get_user_model().objects.create_user(
            username= "expensive",
            password=self.user_data2['password'],
            phone_number=self.user_data2['phone_number'],
            address=self.user_data2['address'],
            email=self.user_data2['email'],
            name=self.user_data2['name'],
            is_active=self.user_data2['is_active']
        )
        test_search = 'ex'
        search_url = f"/api/u_search/{test_search}"
        response = self.client.get(search_url, format="json")
        #import pdb; pdb.set_trace()
        name = list(response.data[0].items())[2][1]
        username = list(response.data[0].items())[0][1]
        email = list(response.data[0].items())[1][1]
        address= list(response.data[0].items())[3][1]
        phone = list(response.data[0].items())[5][1]
        self.assertEqual(response.status_code, 302)
        self.assertEqual(username, 'expensive')
        self.assertEqual(name, f'{self.user_data2["name"]}')
        self.assertEqual(email, f'{self.user_data2["email"]}')
        self.assertEqual(address, f'{self.user_data2["address"]}')
        self.assertEqual(phone, f'{self.user_data2["phone_number"]}')

