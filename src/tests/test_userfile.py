import unittest
from userfile import UserFile
from tests.test_filehandlers import TestFile    # type: ignore
from tests.test_poi_data import TestPoiData     # type: ignore
from poi_data import PoiData


class TestUserFile(unittest.TestCase):
    """Test case for testing the userfile module."""

    def setUp(self):
        """Sets up test UserFile objects.

        Sets up separate UserFile objects with different regions.
        Regions consist of places that exist in search_history and
        new regions. Also utilises setUp variables from the TestPoiData
        class in the test_poi_data module to create test variables
        for a UserFile object's test_read_flag_and_save method.
        """
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
        testclass1 = PoiData(testapidata.place_info1, testapidata.poi_results1)
        testclass1.extract()
        testclass1.consolidate_categories()
        self.test_data = testclass1.place_info

    def tearDown(self):
        """Clean up test files created during setUp/testing."""

        try:
            TestFile.delete_test_file(
                "tests/resources/test/Melbourne-Australia.json")
        except FileNotFoundError:
            pass

    def test_file_instantiation(self):
        """Tests UserFile object instantiation.

        Tests that correctness of instance attributes for
        self.test_file1 and self.test_file2.
        """
        self.assertListEqual(
            self.test_file1.past_searches, self.test_file2.past_searches)
        self.assertNotEqual(self.test_file1.region, self.test_file2.region)
        self.assertEqual(self.test_file1.region, ["New York", "United States"])
        self.assertEqual(self.test_file2.region, ["Delhi", "India"])

    def test_search_and_display_data(self):
        """Tests UserFile object's search_and_display_data method.

        Tests for boolean value returned by using the search_and_display_data
        method for previously saved data and data not previously searched
        and saved.
        """
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
        """Tests UserFile objects read_flag_and_save() method.

        Tests for correct final_format and file_path returned by the
        read_flag_and_save method.
        """
        result = self.test_file4.read_flag_and_save(self.test_data, "city")
        self.assertNotIn("Region", result[0])
        self.assertIn("City", result[0])
        self.assertTrue(self.test_file4.city == result[0]["City"])
        self.assertEqual(
            result[1], "tests/resources/test/Melbourne-Australia.json")
