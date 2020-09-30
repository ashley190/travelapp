import unittest
from userfile import UserFile
from tests.test_filehandlers import TestFile    # type: ignore
from tests.test_poi_data import TestPoiData     # type: ignore
from poi_data import PoiData


class TestUserFile(unittest.TestCase):
    def setUp(self):
        self.test_file1 = UserFile(
            ["New York", "United States"], "tests/resources/test/")
        self.test_file2 = UserFile(
            ["Delhi", "India"], "tests/resources/test/")
        self.test_file3 = UserFile(
            ["Illinois", "United States"], "tests/resources/test/")
        self.test_file3.city = ["Chicago", "United States"]

        # set up for test_read_flag_and_save
        self.test_file4 = UserFile(
            ["Victoria", "Australia"], "tests/resources/test/")
        self.test_file4.city = ["Melbourne", "Australia"]
        testapidata = TestPoiData()
        testapidata.setUp()
        testclass1 = PoiData(testapidata.city_info1, testapidata.poi_results1)
        testclass1.extract()
        testclass1.consolidate_categories()
        self.test_data = testclass1.city_info

    def tearDown(self):
        try:
            TestFile.delete_test_file(
                "tests/resources/test/Melbourne-Australia.json")
        except FileNotFoundError:
            pass

    def test_file_instantiation(self):
        self.assertListEqual(
            self.test_file1.past_searches, self.test_file2.past_searches)
        self.assertNotEqual(self.test_file1.region, self.test_file2.region)

    def test_search_and_display_data(self):
        test1_place = self.test_file1.region
        self.test_file1.searchfile = f"{test1_place[0]}-{test1_place[1]}.json"
        test2_place = self.test_file2.region
        self.test_file2.searchfile = f"{test2_place[0]}-{test2_place[1]}.json"
        test3_place = self.test_file3.city
        self.test_file3.searchfile = f"{test3_place[0]}-{test3_place[1]}.json"
        self.assertTrue(self.test_file1.search_and_display_data(test1_place))
        self.assertFalse(self.test_file2.search_and_display_data(test2_place))
        self.assertTrue(self.test_file3.search_and_display_data(test3_place))

    def test_read_flag_and_save(self):
        result = self.test_file4.read_flag_and_save(self.test_data, "city")
        self.assertNotIn("Region", result[0])
        self.assertIn("City", result[0])
        self.assertTrue(self.test_file4.city == result[0]["City"])
        self.assertEqual(
            result[1], "tests/resources/test/Melbourne-Australia.json")
