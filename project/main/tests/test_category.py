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
        self.assertEqual(long, f'{self.location_data["long"]}.000000000000000')
        self.assertEqual(latt, f'{self.location_data["latt"]}.000000000000000')
        self.assertEqual(place_category, self.location_data["place_category"])

    def test_category_response_objects_are_correct_without_using_category(self):
        location = locations.objects.create(
            name= self.location_data["name"],
            long=self.location_data["long"],
            latt=self.location_data["latt"],
            place_category=self.location_data["place_category"]
        )
        location = locations.objects.create(
            name=self.location_data1["name"],
            long=self.location_data1["long"],
            latt=self.location_data1["latt"],
            place_category=self.location_data1["place_category"]
        )
        location = locations.objects.create(
            name=self.location_data2["name"],
            long=self.location_data2["long"],
            latt=self.location_data2["latt"],
            place_category=self.location_data2["place_category"]
        )
        data = {
            "coordinates": [1,1,6,6],
        }
        res = self.client.post(self.category_url, data, format='json')
        #import pdb; pdb.set_trace()
        name = list(res.data['message'][0].items())[1][1]
        long = list(res.data['message'][0].items())[3][1]
        latt = list(res.data['message'][0].items())[4][1]
        place_category = list(res.data['message'][0].items())[7][1]
        name1 = list(res.data['message'][1].items())[1][1]
        long1 = list(res.data['message'][1].items())[3][1]
        latt1 = list(res.data['message'][1].items())[4][1]
        place_category1 = list(res.data['message'][1].items())[7][1]
        name2 = list(res.data['message'][2].items())[1][1]
        long2 = list(res.data['message'][2].items())[3][1]
        latt2 = list(res.data['message'][2].items())[4][1]
        place_category2 = list(res.data['message'][2].items())[7][1]
        self.assertEqual(res.status_code, 200)
        self.assertEqual(name, f'{self.location_data["name"]}')
        self.assertEqual(long, f'{self.location_data["long"]}.000000000000000')
        self.assertEqual(latt, f'{self.location_data["latt"]}.000000000000000')
        self.assertEqual(place_category, self.location_data["place_category"])
        self.assertEqual(name1, f'{self.location_data1["name"]}')
        self.assertEqual(long1, f'{self.location_data1["long"]}.000000000000000')
        self.assertEqual(latt1, f'{self.location_data1["latt"]}.000000000000000')
        self.assertEqual(place_category1, self.location_data1["place_category"])
        self.assertEqual(name2, f'{self.location_data2["name"]}')
        self.assertEqual(long2, f'{self.location_data2["long"]}.000000000000000')
        self.assertEqual(latt2, f'{self.location_data2["latt"]}.000000000000000')
        self.assertEqual(place_category2, self.location_data2["place_category"])
        self.assertNotEqual(place_category2,place_category,place_category1)


