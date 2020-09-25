import unittest
from unittest.mock import patch
from test_filehandlers import TestFile
from places import Places


class TestPlacesClass(unittest.TestCase):
    def setUp(self):
        TestFile.create_test_json('test.json')
        self.testplaces = Places('test.json')

    def tearDown(self):
        TestFile.delete_test_file('test.json')

    def test_places_attributes(self):
        self.assertEqual(len(self.testplaces.places), 7)
        self.assertEqual(len(self.testplaces.cities_database), 5)
        self.assertIsInstance(self.testplaces.cities_database, dict)
        self.assertEqual(len(self.testplaces.cities_database["United States"]), 2)
        self.assertIsInstance(self.testplaces.cities_database['Japan'], dict)
        self.assertIsInstance(self.testplaces.cities_database['Japan']['Tōkyō'], list)

    @patch('places.TerminalMenu')
    def test_places_selection(self, TerminalMenu):
        instance = TerminalMenu.return_value
        instance.show.side_effect = [0, 0, 2, 1, 4, 0]
        self.assertEqual(self.testplaces.select_region(), ('Tōkyō', 'Japan'))
        self.assertEqual(self.testplaces.select_region(), ('Texas', 'United States'))
        self.assertEqual(self.testplaces.select_region(), ('London, City of', 'United Kingdom'))
