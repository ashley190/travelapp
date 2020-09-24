import unittest
from unittest.mock import Mock
from test_filehandlers import TestFile
from places_db import Places

class TestPlacesClass(unittest.TestCase):
    TestFile.create_test_json('test.json')
    testplaces = Places('test.json')
    TestFile.delete_test_file('test.json')

    def test_places_attributes(self):
        self.assertEqual(len(self.testplaces.places), 7)
        self.assertEqual(len(self.testplaces.cities_database), 5)
        self.assertIsInstance(self.testplaces.cities_database, dict)
        self.assertEqual(len(self.testplaces.cities_database["United States"]), 2)
        self.assertIsInstance(self.testplaces.cities_database['Japan'], dict)
        self.assertIsInstance(self.testplaces.cities_database['Japan']['Tōkyō'], list)
    
    def test_places_selection(self):
        pass