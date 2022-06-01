from .test_setUp import Test_SetUp
from django.contrib.auth import get_user_model
from review.models import locations,review

class Testaddreview(Test_SetUp):
    def test_review_response_with_201(self):
        location = locations.objects.create(
            name= self.location_data["name"],
            long=self.location_data["long"],
            latt=self.location_data["latt"],
            place_category=self.location_data["place_category"]
        )
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=True
        )
        data = {
            "username": self.user_data['username'],
            "password": self.user_data['password'],
        }
        review_data={
            "title":"user2 review",
            "text" : "bad place",
            "is_public":False,
            "user":user.id,
            "location":location.id
        }
        res = self.client.post(self.login_url, data, format='json')

        header = self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % res.json()['access'])
        response = self.client.post(self.review_url,review_data, format="json")
        # import pdb; pdb.set_trace()

        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 201)

    def test_get_location_reviews_with_200_204(self):
        location = locations.objects.create(
            name= self.location_data["name"],
            long=self.location_data["long"],
            latt=self.location_data["latt"],
            place_category=self.location_data["place_category"]
        )
        location1 = locations.objects.create(
            name= self.location_data["name"],
            long=self.location_data["long"],
            latt=self.location_data["latt"],
            place_category=self.location_data["place_category"]
        )
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=True
        )
        review1=review.objects.create(
            title="user2 review",
            text = "bad place",
            is_public=False,
            user=user,
            location=location
        )
        data = {
            "username": self.user_data['username'],
            "password": self.user_data['password'],
        }
        res = self.client.post(self.login_url, data, format='json')
        url=f'/api/get_location_reviews/{location.id}'
        header = self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % res.json()['access'])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        url1=f'/api/get_location_reviews/{location1.id}'
        header = self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % res.json()['access'])
        response = self.client.get(url1, format="json")
        self.assertEqual(response.status_code, 204)

    def test_get_reviews_api_response(self):
        location = locations.objects.create(
            name= self.location_data["name"],
            long=self.location_data["long"],
            latt=self.location_data["latt"],
            place_category=self.location_data["place_category"]
        )
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=True
        )
        data = {
            "username": self.user_data['username'],
            "password": self.user_data['password'],
        }
        review1=review.objects.create(
            title="user2 review",
            text = "bad place",
            is_public=False,
            user=user,
            location=location
        )
        res = self.client.post(self.login_url, data, format='json')
        get_reviews_url = "/api/get_reviews/1"
        header = self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % res.json()['access'])
        response = self.client.get(get_reviews_url, format="json")
        self.assertEqual(response.status_code, 200)

        get_reviews_url = "/api/get_reviews/2"
        header = self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % res.json()['access'])
        response = self.client.get(get_reviews_url, format="json")
        self.assertEqual(response.status_code, 200)

        get_reviews_url = "/api/get_reviews/5"
        header = self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % res.json()['access'])
        response = self.client.get(get_reviews_url, format="json")
        self.assertEqual(response.status_code, 400)

    def test_category_response_with_200(self):
        location = locations.objects.create(
            name= self.location_data["name"],
            long=self.location_data["long"],
            latt=self.location_data["latt"],
            place_category=self.location_data["place_category"]
        )
        data = {
            "coordinates": [1,1,5,5],
        }
        get_map_location_url = "/api/get_map_locations"
        res = self.client.post(get_map_location_url, data, format='json')
        #import pdb; pdb.set_trace()
        self.assertEqual(res.status_code, 200)

        get_map_locations_url = "/api/get_map_location_reviews"
        res = self.client.post(get_map_locations_url, data, format='json')
        #import pdb; pdb.set_trace()
        self.assertEqual(res.status_code, 200)
    

    def test_user_can_successfully_add_rivew(self):
        res= self.client.post(self.register_url,self.user_data,format='json')
        #import pdb; pdb.set_trace()
        self.assertEqual(res.data['message']['username'], self.user_data['username'])
        self.assertEqual(res.data['message']['email'], self.user_data['email'])
        self.assertEqual(res.data['message']['phone_number'], self.user_data['phone_number'])
        self.assertEqual(res.data['message']['address'], self.user_data['address'])
        self.assertEqual(res.data['message']['name'], self.user_data['name'])
        self.assertEqual(res.data['message']['is_active'], self.user_data['is_active'])
        self.assertEqual(res.status_code,201)

    def test_user_shouldnot_add_samee_review(self):
        user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
            address=self.user_data['address'],
            email=self.user_data['email'],
            name=self.user_data['name'],
            is_active=self.user_data['is_active']
        )
        res= self.client.post(self.register_url,self.user_data,format='json')
        self.assertEqual(res.status_code,400)
