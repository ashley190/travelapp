import unittest
from unittest.mock import Mock, patch
from get_poi import TripAdvisorApi
import sys
from file_handler import JsonHandler


class TestApiGet(unittest.TestCase):
    """Test case for testing TripAdvisorApi instance methods."""

    def setUp(self):
        """Sets up testing variables.

        Test data using test API query outputs for location and poi searches.
        """
        # used in test_location_search and test_get_poi
        self.test1: TripAdvisorApi = TripAdvisorApi(
            ["Lima", "Peru"], ["Lima", "Peru"])
        self.test2: TripAdvisorApi = TripAdvisorApi(
            ["fake_reg", "fake_country"], ["fake_city", "fake_country"])
        self.data: list = JsonHandler.read_json(
            "tests/resources/test-loc-data.json")
        self.poidata: list = JsonHandler.read_json(
            "tests/resources/test-poi-data.json")

        # used in test_poi_search
        self.region_info1: dict = {
            "name": "Victoria",
            "location_id":
            "255098"
            }
        self.poi_info1: dict = {
            'errors': [{
                'type': 'BadRequestException',
                'message': 'Cannot view this connection at this level.',
                'code': '120'}]
                }
        self.region_info2: dict = {
            'name': 'Melbourne',
            'location_id': '255100',
            'description': 'Some description about Melbourne'
            }
        self.poi_info2: list = JsonHandler.read_json(
            "tests/resources/test-poi-search.json")

    @patch("get_poi.ApiQuery")
    def test_location_search(self, ApiQuery):
        """Tests a TripAdvisorApi object's location_search() method.

        Tests location_result method output for a mock successful and
        unsuccessful search.

        Args:
            ApiQuery (MockObject): Mock object to mock different API responses.
        """
        instance = ApiQuery.return_value
        instance.get_data.side_effect = [
            (200, self.data), (400, "Request Error")
            ]
        test1_location_result: dict = self.test1.location_search(
            self.test1.region_and_country)
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
        """Tests a TripAdvisorApi object's get_poi() method.

        Tests get_poi() method output for a mocked successful and
        unsuccessful query.

        Args:
            ApiQuery (MockObject): Mock object to mock different API responses
        """
        instance = ApiQuery.return_value
        instance.get_data.side_effect = [
            (200, self.poidata), (400, "Request Error")
            ]
        test1_poi_result: dict = self.test1.get_poi("test_id")
        self.assertIsInstance(test1_poi_result, dict)
        self.assertIsInstance(test1_poi_result["data"], list)
        self.assertEqual(len(test1_poi_result["data"]), 33)
        # test unsuccessful query
        sys.exit = Mock()
        test2_poi_result: dict = self.test2.get_poi("test_id2")
        self.assertEqual(test2_poi_result, "Request Error")
        sys.exit.assert_called_once()

    @patch.object(TripAdvisorApi, "location_search")
    @patch.object(TripAdvisorApi, "get_poi")
    def test_poi_search(self, get_poi, location_search):
        """Tests a TripAdvisor object's poi_search() method.

        Tests that the correct level search is conducted when "error"
        is encountered in a regional/state level search.

        Args:
            get_poi (patch object): Patched get_poi method to return different
                subsequent output values.
            location_search (patch object): Patched location_search method to
                return different subsequent output values.
        """
        location_search.side_effect = [self.region_info1, self.region_info2]
        get_poi.side_effect = [self.poi_info1, self.poi_info2]
        test1 = TripAdvisorApi(
            ["Victoria", "Australia"], ["Melbourne", "Australia"])
        result: tuple = test1.poi_search()
        self.assertTrue(result[2] == "city")
        self.assertTrue(result[0]["name"] == "Melbourne")
        self.assertIsInstance(result[0], dict)
        self.assertIsInstance(result[1], dict)
        self.assertIsInstance(result[2], str)
        self.assertEqual(len(result[0]), 3)
        self.assertEqual(len(result[1]["data"]), 33)
