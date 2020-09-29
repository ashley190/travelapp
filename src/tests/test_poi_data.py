import unittest
from poi_data import PoiData
from file_handler import JsonHandler


class TestPoiData(unittest.TestCase):
    def setUp(self):
        self.city_info1 = {
            'name': 'Melbourne',
            'location_id': '255100',
            'description': 'Some description about Melbourne'
            }
        self.poi_results1 = JsonHandler.read_json(
            "tests/resources/test-poi-search.json")

    def testpoidata(self):
        testclass1 = PoiData(self.city_info1, self.poi_results1)
        self.assertEqual(len(testclass1.poi_results), 33)
        self.assertTrue("poi" not in testclass1.city_info)
        self.assertTrue(len(testclass1.poi_results[0]) > 9)
        testclass1.extract()
        self.assertEqual(len(testclass1.city_info["pois"]), 30)
        self.assertTrue("pois" in testclass1.city_info)
        self.assertTrue(len(testclass1.city_info["pois"][0]) <= 9)
        self.assertTrue("subcategory" in testclass1.city_info["pois"][0])
        self.assertTrue("subtype" in testclass1.city_info["pois"][0])
        testclass1.consolidate_categories()
        self.assertTrue("subcategory" not in testclass1.city_info["pois"][0])
        self.assertTrue("subtype" not in testclass1.city_info["pois"][0])
