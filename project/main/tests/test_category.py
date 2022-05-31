from .test_setUp import Test_SetUp
from review.models import locations

class TestCategory(Test_SetUp):
    def test_category_response_with_200(self):
        location = locations.objects.create(
            name= self.location_data["name"],
            long=self.location_data["long"],
            latt=self.location_data["latt"],
            place_category=self.location_data["place_category"]
        )
        data = {
            "coordinates": [1,1,5,5],
            "place_category": 3
        }
        res = self.client.post(self.category_url, data, format='json')
        #import pdb; pdb.set_trace()
        self.assertEqual(res.status_code, 200)

    def test_category_response_objects_are_correct(self):
        location = locations.objects.create(
            name= self.location_data["name"],
            long=self.location_data["long"],
            latt=self.location_data["latt"],
            place_category=self.location_data["place_category"]
        )
        data = {
            "coordinates": [1,1,5,5],
            "place_category": 3
        }
        res = self.client.post(self.category_url, data, format='json')
        name = list(res.data['message'][0].items())[1][1]
        long = list(res.data['message'][0].items())[3][1]
        latt = list(res.data['message'][0].items())[4][1]
        place_category = list(res.data['message'][0].items())[7][1]
        #import pdb; pdb.set_trace()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(name, f'{self.location_data["name"]}')
        self.assertEqual(long, f'{self.location_data["long"]}00000000000000')
        self.assertEqual(latt, f'{self.location_data["latt"]}00000000000000')
        self.assertEqual(place_category, self.location_data["place_category"])


