from file_handler import *
import csv
import os
import unittest


class TestFile:
    data = [
        ["Tokyo", "Tokyo", "35.6850", "139.7514", "Japan", "JP", "JPN", "Tōkyō", "primary", "35676000", "1392685764"],
        ["Mexico City", "Mexico City", "19.4424", "-99.1310", "Mexico", "MX", "MEX", "Ciudad de México", "primary", "19028000", "1484247881"],
        ["Los Angeles", "Los Angeles", "34.1139", "-118.4068", "United States", "US", "USA", "California", "", "12815475.0", "1840020491"],
        ["Paris", "Paris", "48.8667", "2.3333", "France", "FR", "FRA", "Île-de-France", "primary", "9904000", "1250015082"],
        ["Austin", "Austin", "30.3006", "-97.7517", "United States", "US", "USA", "Texas", "admin", "1638716.0", "1840019590"],
        ["Arlington", "Arlington", "32.6998", "-97.1251", "United States", "US", "USA", "Texas", "", "396394", "1840019422"],
        ["London", "London", "51.5000", "-0.1167", "United Kingdom", "GB", "GBR", "London, City of", "primary", "8567000", "1826645935"]
    ]

    @classmethod
    def create_file(cls):
        with open("test.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["city", "city_ascii", "lat", "lng", "country", "iso2", "iso3", "admin_name", "capital", "population", "id"])
            writer.writerows(cls.data)

    @classmethod
    def delete_test_file(cls, *file_path):
        for file in file_path:
            os.remove(file)

    @classmethod
    def create_test_json(cls, file_path):
        cls.create_file()
        test_data = CsvHandler.read_csv('test.csv')
        JsonHandler.write_json(file_path, test_data)
        cls.delete_test_file('test.csv')


class TestFileHandlers(unittest.TestCase):
    def setUp(self):
        TestFile.create_file()
        self.test_list = CsvHandler.read_csv("test.csv")
        self.test_list_2 = CsvHandler.read_csv("")
        FileConverter.save_csv_as_json("test.csv", "test.json")
        self.text_from_json = JsonHandler.read_json("test.json")
        self.text_from_blank = JsonHandler.read_json("fake.json")

    def tearDown(self):
        TestFile.delete_test_file("test.csv", "test.json")

    def test_read_csv(self):
        self.assertEqual(len(self.test_list), 7)
        self.assertEqual((self.test_list[0]["city_ascii"], self.test_list[0]["country"], self.test_list[0]["admin_name"]), ("Tokyo", "Japan", "Tōkyō"))
        self.assertEqual((self.test_list[3]["city_ascii"], self.test_list[3]["country"], self.test_list[3]["admin_name"]), ("Paris", "France", "Île-de-France"))
        self.assertEqual((self.test_list_2), None)

    def test_save_csv_as_json(self):
        self.assertEqual((self.text_from_json[1]["city_ascii"], self.text_from_json[1]["country"], self.text_from_json[1]["admin_name"]), ("Mexico City", "Mexico", "Ciudad de México"))
        self.assertEqual((self.text_from_json[4]["city_ascii"], self.text_from_json[4]["country"], self.text_from_json[4]["admin_name"]), ("Austin", "United States", "Texas"))
        self.assertEqual((self.text_from_blank), [])
