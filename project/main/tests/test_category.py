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

