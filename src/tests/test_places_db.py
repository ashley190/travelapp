import unittest
from unittest.mock import MagicMock, Mock,patch
from test_filehandlers import TestFile
from places_db import Places, TerminalMenu
# from simple_term_menu import TerminalMenu   # type: ignore


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

    # @patch('places_db.TerminalMenu.show', side_effect=[0, 0, 2, 1, 4, 0])
    @patch('places_db.TerminalMenu')
    def test_places_selection(self, termmenu):
        with patch.object(termmenu, 'show', side_effect=[0, 0, 2, 1, 4, 0]):
        # print(self.testplaces.cities_database)
            print(self.testplaces.select_country_and_city())
            self.assertEqual(self.testplaces.select_country_and_city(), ('Tōkyō', 'Japan'))
        # self.assertEqual(self.testplaces.select_country_and_city(), ('Texas', 'United States'))
        # self.assertEqual(self.testplaces.select_country_and_city(), ('London, City of', 'United Kingdom'))
