import unittest
from unittest.mock import patch
from users import User
from tests.test_filehandlers import TestFile    # type: ignore


class TestUserClass(unittest.TestCase):
    @patch("builtins.input",
           side_effect=["testuser1", "key123", "testuser2", "key456"])
    def setUp(self, mock_input):
        self.testuser1 = User()
        self.testuser1.set_API_key("test1")
        self.testuser2 = User()
        self.testuser2.set_API_key("test2")

    def tearDown(self):
        TestFile.delete_test_file("test1", "test2")

    def test_user_instantiation(self):
        self.assertTrue(self.testuser1.name == "testuser1")
        self.assertTrue(self.testuser2.name == "testuser2")
        self.assertTrue(self.testuser1.path == "resources/testuser1/")
        self.assertTrue(self.testuser2.path == "resources/testuser2/")

    def test_save_api(self):
        with open("test1", "r") as file:
            self.assertEqual(file.read(), "API_KEY=key123")
        with open("test2", "r") as file:
            self.assertEqual(file.read(), "API_KEY=key456")

    def test_api_key_check(self):
        self.assertTrue(self.testuser1.API_key_check("test1"))
        self.assertFalse(self.testuser2.API_key_check("fake"))
