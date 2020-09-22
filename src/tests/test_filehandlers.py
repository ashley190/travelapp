from File_Handler import CsvHandler
import csv
import os
import unittest


class TestFile:
    data = [
        ["Tokyo", "Tokyo", "35.6850", "139.7514", "Japan", "JP", "JPN", "Tōkyō", "primary", "35676000", "1392685764"],
        ["Mexico City", "Mexico City", "19.4424", "-99.1310", "Mexico", "MX", "MEX", "Ciudad de México", "primary", "19028000", "1484247881"],
        ["Los Angeles", "Los Angeles", "34.1139", "-118.4068", "United States", "US", "USA", "California", "", "12815475.0", "1840020491"],
        ["Paris", "Paris", "48.8667", "2.3333", "France", "FR", "FRA", "Île-de-France", "primary", "9904000", "1250015082"],
        ["London", "London", "51.5000", "-0.1167", "United Kingdom", "GB", "GBR", "London, City of", "primary", "8567000", "1826645935"]
    ]

    @classmethod
    def create_file(cls):
        with open('test.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["city", "city_ascii", "lat", "lng", "country", "iso2", "iso3", "admin_name", "capital", "population", "id"])
            writer.writerows(cls.data)

    @classmethod
    def delete_test_file(cls):
        os.remove('test.csv')


class TestCsvHandlerClass(unittest.TestCase):
    def test_read_csv(self):
        TestFile.create_file()
        test_list = CsvHandler.read_csv('test.csv')
        TestFile.delete_test_file()
        print(type(test_list))
