from users import User
from test_filehandlers import TestFile
import unittest
from unittest.mock import patch


class TestUserClass(unittest.TestCase):
    @patch("builtins.input",
           side_effect=["testuser1", "Groot", "Ares", "key1", "key2"])
    def test_user_instantiation(self, User):
        testuser1 = User()
        testuser2 = User()
        testuser3 = User()
        self.assertTrue(testuser1 == "testuser1")
        self.assertTrue(testuser2 == "Groot")
        self.assertTrue(testuser3 == "Ares")

    @patch("builtins.input",
           side_effect=["testuser1", "key123", "testuser2", "key456"])
    def setUp(self, mock_input):
        self.testuser1 = User()
        self.testuser1.set_API_key("test1")
        self.testuser2 = User()
        self.testuser2.set_API_key("test2")

    def tearDown(self):
        TestFile.delete_test_file("test1", "test2")

    def test_save_api(self):
        with open("test1", "r") as file:
            self.assertEqual(file.read(), "API_KEY=key123")
        with open("test2", "r") as file:
            self.assertEqual(file.read(), "API_KEY=key456")
