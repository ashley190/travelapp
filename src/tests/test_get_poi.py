import unittest
from unittest.mock import Mock, patch
from get_poi import TripAdvisorApi
import sys
from file_handler import JsonHandler


class TestApiGet(unittest.TestCase):
    def setUp(self):
        self.data = JsonHandler.read_json("tests/resources/test-loc-data.json")
        self.poidata = JsonHandler.read_json(
            "tests/resources/test-poi-data.json")
        self.region_info1 = {
            "name": "Victoria",
            "location_id":
            "255098"
            }
        self.poi_info1 = {
            'errors': [{
                'type': 'BadRequestException',
                'message': 'Cannot view this connection at this level.',
                'code': '120'}]
                }
        self.region_info2 = {
            'name': 'Melbourne',
            'location_id': '255100',
            'description': 'Some description about Melbourne'
            }
        self.poi_info2 = JsonHandler.read_json(
            "tests/resources/test-poi-search.json")
        self.test1 = TripAdvisorApi(
            ["Lima", "Peru"], ["Lima", "Peru"])
        self.test2 = TripAdvisorApi(
            ["fake_reg", "fake_country"], ["fake_city", "fake_country"])

    @patch("get_poi.ApiQuery")
    def test_location_search(self, ApiQuery):
        instance = ApiQuery.return_value
        instance.get_data.side_effect = [
            (200, self.data), (400, "Request Error")
            ]
        test1_location_result = self.test1.location_search(
            self.test1.region_and_country)
        print(test1_location_result)
        self.assertIsInstance(test1_location_result, dict)
        self.assertEqual(len(test1_location_result), 3)
        self.assertTrue(test1_location_result["name"] == "Lima")

        sys.exit = Mock()
        try:
            self.test2.location_search(self.test2.region_and_country)
        except TypeError:
            sys.exit.assert_called_once()

    @patch("get_poi.ApiQuery")
    def test_get_poi(self, ApiQuery):
        instance = ApiQuery.return_value
        instance.get_data.side_effect = [
            (200, self.poidata), (400, "Request Error")
            ]
        test1_poi_result = self.test1.get_poi("test_id")
        self.assertIsInstance(test1_poi_result, dict)
        self.assertIsInstance(test1_poi_result["data"], list)
        self.assertEqual(len(test1_poi_result["data"]), 33)

        sys.exit = Mock()
        test2_poi_result = self.test2.get_poi("test_id2")
        self.assertEqual(test2_poi_result, "Request Error")
        sys.exit.assert_called_once()

    @patch.object(TripAdvisorApi, "location_search")
    @patch.object(TripAdvisorApi, "get_poi")
    def test_poi_search(self, get_poi, location_search):
        location_search.side_effect = [self.region_info1, self.region_info2]
        get_poi.side_effect = [self.poi_info1, self.poi_info2]
        test1 = TripAdvisorApi(
            ["Victoria", "Australia"], ["Melbourne", "Australia"])
        result = test1.poi_search()
        self.assertTrue(result[2] == "city")
        self.assertTrue(result[0]["name"] == "Melbourne")
        self.assertIsInstance(result[0], dict)
        self.assertIsInstance(result[1], dict)
        self.assertIsInstance(result[2], str)
        self.assertEqual(len(result[0]), 3)
        self.assertEqual(len(result[1]["data"]), 33)
