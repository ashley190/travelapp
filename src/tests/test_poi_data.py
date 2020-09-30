import unittest
from poi_data import PoiData
from file_handler import JsonHandler


class TestPoiData(unittest.TestCase):
    """Test case for testing a PoiData object"""

    def setUp(self):
        """Sets up variables for object creation and testing."""
        self.place_info1: dict = {
            'name': 'Melbourne',
            'location_id': '255100',
            'description': 'Some description about Melbourne'
            }
        self.poi_results1: list = JsonHandler.read_json(
            "tests/resources/test-poi-search.json")

    def testpoidata(self):
        """Tests PoiData object instantiation and methods.

        Test instance attributes of a PoiData object prior to and after
        running the extract() and consolidate_categories() methods.
        """
        testclass1 = PoiData(self.place_info1, self.poi_results1)
        self.assertEqual(len(testclass1.poi_results), 33)
        self.assertTrue("poi" not in testclass1.place_info)
        self.assertTrue(len(testclass1.poi_results[0]) > 9)
        testclass1.extract()
        self.assertEqual(len(testclass1.place_info["pois"]), 30)
        self.assertTrue("pois" in testclass1.place_info)
        self.assertTrue(len(testclass1.place_info["pois"][0]) <= 9)
        self.assertTrue("subcategory" in testclass1.place_info["pois"][0])
        self.assertTrue("subtype" in testclass1.place_info["pois"][0])
        testclass1.consolidate_categories()
        self.assertTrue("subcategory" not in testclass1.place_info["pois"][0])
        self.assertTrue("subtype" not in testclass1.place_info["pois"][0])
