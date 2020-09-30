import unittest
from unittest.mock import patch
from test_filehandlers import TestFile
from places import Places, Database


class TestCitiesDbClass(unittest.TestCase):
    """Tests Database object instantiation"""

    def setUp(self):
        """Sets up and instantiate Database object using TestFile attributes
        and methods.
        """
        TestFile.create_test_json()
        self.testplaces = Database("tests/test.json")

    def tearDown(self):
        """Cleans up files created during setUp.
        """
        TestFile.delete_test_file("tests/test.json")

    def test_database_creation(self):
        """Tests Database object instantiation.

        Tests for correct data structures and data in the
        self.testplaces object.
        """
        self.assertIsInstance(self.testplaces.cities_db, dict)
        self.assertIsInstance(self.testplaces.cities_db["Japan"], dict)
        self.assertIsInstance(
            self.testplaces.cities_db["Mexico"]["Ciudad de México"], list)
        self.assertIn(
            "California", self.testplaces.cities_db["United States"])
        self.assertIn(
            "Paris", self.testplaces.cities_db["France"]["Île-de-France"])


class TestPlacesClass(unittest.TestCase):
    """Tests attributes and instance methods found in a Places object."""

    def setUp(self):
        """Set up Places object with test data."""

        TestFile.create_test_json()
        self.testplaces: Places = Places("tests/test.json")

    def tearDown(self):
        """Clean up files created during setUp or testing."""
        TestFile.delete_test_file("tests/test.json")

    def test_places_attributes(self):
        """Test Places object attributes.

        Checks for correct data structures and data in Places object attributes
        """
        self.assertEqual(len(self.testplaces.places), 7)
        self.assertEqual(len(self.testplaces.cities_db), 5)
        self.assertIsInstance(self.testplaces.cities_db, dict)
        self.assertEqual(
            len(self.testplaces.cities_db["United States"]), 2)
        self.assertIsInstance(self.testplaces.cities_db["Japan"], dict)
        self.assertIsInstance(
            self.testplaces.cities_db["Japan"]["Tōkyō"], list)

    @patch("places.TerminalMenu")
    def test_select_region(self, TerminalMenu):
        """Tests select_region() method in Places object.

        Tests for correct output from the select_region() method given
        each mocked user selection.

        Args:
            TerminalMenu (Mock Object): Mock object to mock user selection
                on Terminal Menu.
        """
        instance = TerminalMenu.return_value
        instance.show.side_effect = [0, 0, 2, 1, 4, 0]
        self.assertEqual(self.testplaces.select_region(), ["Tōkyō", "Japan"])
        self.assertEqual(self.testplaces.select_region(),
                         ["Texas", "United States"])
        self.assertEqual(self.testplaces.select_region(),
                         ["London, City of", "United Kingdom"])

    @patch("places.TerminalMenu")
    def test_select_city(self, TerminalMenu):
        """Tests select_city method in Places object.

        Tests for correct output from the select_city() method given
        pre-determined region info and mocked user selection

        Args:
            TerminalMenu (Mock Object): Mocked object to mock user selection
                on TerminalMenu
        """
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
