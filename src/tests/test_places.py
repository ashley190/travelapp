import unittest
from unittest.mock import patch
from test_filehandlers import TestFile
from places import Places, Database


class TestCitiesDbClass(unittest.TestCase):
    def setUp(self):
        TestFile.create_test_json("test.json")
        self.testplaces = Database("test.json")

    def tearDown(self):
        TestFile.delete_test_file("test.json")

    def test_database_creation(self):
        self.assertIsInstance(self.testplaces.cities_db, dict)
        self.assertIsInstance(self.testplaces.cities_db["Japan"], dict)
        self.assertIsInstance(
            self.testplaces.cities_db["Mexico"]["Ciudad de México"], list)
        self.assertIn(
            "California", self.testplaces.cities_db["United States"])
        self.assertIn(
            "Paris", self.testplaces.cities_db["France"]["Île-de-France"])


class TestPlacesClass(unittest.TestCase):
    def setUp(self):
        TestFile.create_test_json("test.json")
        self.testplaces = Places("test.json")

    def tearDown(self):
        TestFile.delete_test_file("test.json")

    def test_places_attributes(self):
        self.assertEqual(len(self.testplaces.places), 7)
        self.assertEqual(len(self.testplaces.cities_db), 5)
        self.assertIsInstance(self.testplaces.cities_db, dict)
        self.assertEqual(
            len(self.testplaces.cities_db["United States"]), 2)
        self.assertIsInstance(self.testplaces.cities_db["Japan"], dict)
        self.assertIsInstance(
            self.testplaces.cities_db["Japan"]["Tōkyō"], list)

    @patch("places.TerminalMenu")
    def test_region_selection(self, TerminalMenu):
        instance = TerminalMenu.return_value
        instance.show.side_effect = [0, 0, 2, 1, 4, 0]
        self.assertEqual(self.testplaces.select_region(), ["Tōkyō", "Japan"])
        self.assertEqual(self.testplaces.select_region(),
                         ["Texas", "United States"])
        self.assertEqual(self.testplaces.select_region(),
                         ["London, City of", "United Kingdom"])

    @patch("places.TerminalMenu")
    def test_city_selection(self, TerminalMenu):
        instance = TerminalMenu.return_value
        instance.show.side_effect = [0, 1, 0]
        selected_region_1 = ("Ciudad de México", "Mexico")
        selected_region_2 = ("Texas", "United States")
        selected_region_3 = ("Île-de-France", "France")
        self.assertEqual(self.testplaces.select_city(selected_region_1),
                         ["Mexico City", "Mexico"])
        self.assertEqual(self.testplaces.select_city(selected_region_2),
                         ["Arlington", "United States"])
        self.assertEqual(self.testplaces.select_city(selected_region_3),
                         ["Paris", "France"])
