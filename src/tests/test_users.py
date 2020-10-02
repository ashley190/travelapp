import unittest
from unittest.mock import patch, Mock
from users import User, os
from tests.test_filehandlers import TestFile    # type: ignore


class TestUserClass(unittest.TestCase):
    """Test case for testing User objects."""

    @patch("builtins.input",
           side_effect=["key123", "testuser1", "key456", "testuser2"])
    def setUp(self, mock_input: str):
        """Sets up test variables for testing of User object.

        Args:
            mock_input (str): mock user inputs each time builtins.input
                is called. Sequence of input determined by patch side effects.
        """
        os.execl = Mock()
        self.testuser1 = User(test=True)
        self.testuser1.set_API_key("test1")
        self.testuser1.set_attributes()
        self.testuser2 = User(test=True)
        self.testuser2.set_API_key("test2")
        self.testuser2.set_attributes()

    def tearDown(self):
        """Clean up test files created during setUp and testing."""

        TestFile.delete_test_file("test1", "test2")

    def test_set_attributes(self):
        """Tests User object instantiation.

        Tests for presence and correctness of instance attributes of
        test variables.
        """
        self.assertTrue(self.testuser1.name == "testuser1")
        self.assertTrue(self.testuser2.name == "testuser2")
        self.assertTrue(self.testuser1.path == "resources/testuser1/")
        self.assertTrue(self.testuser2.path == "resources/testuser2/")

    def test_api_key_check(self):
        """Tests User object's API_key_check() method.

        Tests the presence API keys in the correct files using the
        key_exist boolean value returned by the API_key_check() method.
        """
        self.assertTrue(self.testuser1.API_key_check("test1"))
        self.assertFalse(self.testuser2.API_key_check("fake"))

    def test_save_api(self):
        """Tests User object's set_api_key() method.

        Tests that the correct keys are saved to the correct files.
        """
        with open("test1", "r") as file:
            self.assertEqual(file.read(), "API_KEY=key123")
        with open("test2", "r") as file:
            self.assertEqual(file.read(), "API_KEY=key456")
